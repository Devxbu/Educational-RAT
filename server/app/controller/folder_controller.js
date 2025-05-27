const Folder = require('../model/folders');
const File = require('../model/files');
const crypto = require('crypto');
const archiver = require('archiver');
const { S3Client, PutObjectCommand, GetObjectCommand, DeleteObjectCommand } = require('@aws-sdk/client-s3');
const { getSignedUrl } = require('@aws-sdk/s3-request-presigner')

const bucket_name = process.env.BUCKET_NAME;
const bucket_region = process.env.BUCKET_REGION;
const access_key = process.env.ACCESS_KEY;
const secret_access_key = process.env.SECRET_ACCESS_KEY;

const s3 = new S3Client({
    credentials: {
        accessKeyId: access_key,
        secretAccessKey: secret_access_key
    },
    region: bucket_region
});

const handle_errors = (res, error, message = 'An error generated.') => {
    console.error(error);
    return res.status(500).json({ error: message });
};

const random_file_name = (bytes = 32) => crypto.randomBytes(bytes).toString('hex');

module.exports.listRootFolders = async (req, res) => {
    try {
        const folders = await Folder.find({ parent: null });
        return res.status(200).json(folders);
    } catch (error) {
        return handle_errors(res, error, "Error fetching root folders");
    }
}

module.exports.listFiles = async (req, res) => {
    try {
        const folders = await Folder.findById(req.params.id);
        return res.status(200).json(folders);
    } catch (error) {
        return handle_errors(res, error, "Error fetching folders");
    }
}

module.exports.deleteFolder = async (req, res) => {
    try {
        const folder = await Folder.findById(req.params.id);
        const folders = await Folder.find({ parent: req.params.id });

        const files = await File.find({ _id: { $in: folder.files } });
        await Promise.all(files.map(async (file) => {
            await file.deleteOne();
        }));

        folders.forEach(async folder => {
            var files = await File.find({ _id: { $in: folder.files } });
            await Promise.all(files.map(async (file) => {
                await file.deleteOne();
            }));    
        });

        const parent = await Folder.findById(folder.parent);

        if (parent && parent.folders) {
            parent.folders = parent.folders.filter(f => f.toString() !== req.params.id);
            await parent.save();
        }
        await Promise.all(folders.map(async (folder) => {
            await folder.deleteOne();
        }));
        await folder.deleteOne();
        return res.status(200).send();
    } catch (error) {
        return handle_errors(res, error, "Error deleting folder");
    }
}

module.exports.createFolder = async (req, res) => {
    console.log(req.body);
    try {
        if (req.body.parent) {
            const parent = await Folder.findById(req.body.parent);
            if (!parent) return res.status(404).json({ error: "Parent folder not found" });
        }
        const folder = new Folder({
            name: req.body.name,
            parent: req.body.parent || null
        });
        await folder.save();

        if (req.body.parent) {
            const parent = await Folder.findById(req.body.parent);
            parent.folders.push(folder._id);
            await parent.save();
        }

        return res.status(200).json(folder);
    } catch (error) {
        return handle_errors(res, error, "Error creating folder");
    }
}

module.exports.createFile = async (req, res) => {
    const folder_id = req.params.id
    if (req.file) {
        const file_name = random_file_name();

        const params = {
            Bucket: bucket_name,
            Key: file_name,
            Body: req.file.buffer,
            ContentType: req.file.mimetype,
        };

        const command = new PutObjectCommand(params);
        await s3.send(command);

        const new_file = new File({
            file_name: file_name,
            name: req.file.originalname,
            file_type: req.file.mimetype
        });

        await new_file.save();

        const folder = await Folder.findById(folder_id);
        folder.files.push(new_file._id);
        await folder.save();


        return res.status(200).json(new_file);
    }
}

async function appendFolderToZip(zip, folder, parentPath = "") {
    const folderPath = parentPath ? `${parentPath}/${folder.name}` : folder.name;

    const folderFiles = await File.find({ _id: { $in: folder.files } });
    for (const file of folderFiles) {
        const command = new GetObjectCommand({
            Bucket: bucket_name,
            Key: file.file_name
        });

        const response = await s3.send(command);
        zip.append(response.Body, { name: `${folderPath}/${file.name}` });
    }

    const subFolders = await Folder.find({ parent: folder._id });
    for (const subFolder of subFolders) {
        await appendFolderToZip(zip, subFolder, folderPath);
    }
}

module.exports.downloadFolder = async (req, res) => {
    const id = req.params.id;
    console.log(id);
    try {
        const rootFolder = await Folder.findById(id);
        if (!rootFolder) return res.status(404).json({ error: "Folder not found" });

        res.setHeader("Content-Type", "application/zip");
        res.setHeader("Content-Disposition", `attachment; filename="${rootFolder.name}.zip"`);

        const archive = archiver('zip', { zlib: { level: 9 } });
        archive.on('error', err => {
            throw err;
        });

        archive.pipe(res);

        await appendFolderToZip(archive, rootFolder);

        await archive.finalize();

    } catch (err) {
        console.error(err);
        return res.status(500).json({ error: "Download failed" });
    }
};

