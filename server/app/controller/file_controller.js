const File = require('../model/files')
const crypto = require('crypto');
const { S3Client, PutObjectCommand, GetObjectCommand, DeleteObjectCommand } = require('@aws-sdk/client-s3');
const { getSignedUrl } = require('@aws-sdk/s3-request-presigner')

// Bucket constants
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

// Error handler
const handle_errors = (res, error, message = 'An error generated.') => {
    console.error(error);
    return res.status(500).json({ error: message });
};

// Generate random names for files
const random_file_name = (bytes = 32) => crypto.randomBytes(bytes).toString('hex');

module.exports.uploadFile = async (req, res) => {
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
        return res.status(200).json(new_file);
    }
};

module.exports.downloadFile = async (req, res) => {
    const id = req.params.id;

    try {
        const file = await File.findById(id);
        if (!file) return res.status(404).json({ error: "File not found" });

        const command = new GetObjectCommand({
            Bucket: bucket_name,
            Key: file.file_name
        });

        const response = await s3.send(command);

        // Dosya ismi düzgünce ayarlanırsa indirme adı net olur
        res.setHeader("Content-Disposition", `attachment; filename="${file.name || file.file_name}"`);
        res.setHeader("Content-Type", response.ContentType || "application/octet-stream");

        // Pipe ile response doğrudan tarayıcıya akıtılır
        response.Body.pipe(res);

    } catch (err) {
        console.error(err);
        return res.status(500).json({ error: "Download failed" });
    }
};

module.exports.deleteFile = async (req, res) => {
    const id = req.params.id;

    try {
        const file = await File.findById(id);

        if (!file) return res.status(404).json({ error: "File is not found" });

        const delete_params = {
            Bucket: bucket_name,
            Key: file.file_name
        };

        const command = new DeleteObjectCommand(delete_params);
        await s3.send(command);
        await file.deleteOne();

        return res.status(204).send();
    } catch (err) {
        return handle_errors(res, err, "Error");
    }
};


module.exports.listFiles = async (req, res) => {
    try {
        let { page, limit } = req.query;

        page = parseInt(page) || 1;
        limit = parseInt(page) || 10;
        const skip = (page - 1) * limit;

        const total_files = await File.countDocuments();
        const files = await File.find().skip(skip).limit(limit);

        await Promise.all(files.map(async (file) => {
            if (file.file_name) {
                const getObjectParams = {
                    Bucket: bucket_name,
                    Key: file.file_name
                };
                const command = new GetObjectCommand(getObjectParams);
                file.file_name = await getSignedUrl(s3, command, { expiresIn: 3600 });
            };
        }));

        return res.status(200).json({
            current_page: page,
            total_pages: Math.ceil(total_files / limit),
            total_files,
            files
        });
    } catch (error) {
        return handle_errors(res, error, "Generated error when fetching the files");
    }
}

module.exports.searchFile = async (req, res) => {
    const { search } = req.query;

    try {
        const page = parseInt(req.query.page) || 1;
        const limit = parseInt(req.query.limit) || 10;
        const skip = (page - 1) * limit;

        let filter = { name: { $regex: search, $options: "i" } };

        const files = await File.find(filter).skip(skip).limit(limit);
        const total_files = await File.countDocuments(filter);

        await Promise.all(files.map(async (file) => {
            if (file.file_name) {
                const getObjectParams = {
                    Bucket: bucket_name,
                    Key: file.file_name
                };
                const command = new GetObjectCommand(getObjectParams);
                file.file_name = await getSignedUrl(s3, command, { expiresIn: 3600 });
            };
        }));

        return res.status(200).json({
            current_page: page,
            total_pages: Math.ceil(total_files / limit),
            total_files,
            files
        });
    } catch (error) {
        handle_errors(res, error, "File fetching failed");
    }
};