const express = require("express");
const multer = require('multer');
const { listRootFolders, listFiles, deleteFolder, createFolder, createFile, downloadFolder } = require("../controller/folder_controller");

const router = express.Router();

const storage = multer.memoryStorage();
const upload = multer({ storage: storage });

router.get("/root", upload.none(), listRootFolders);
router.get("/list/:id", upload.none(), listFiles);
router.delete("/delete/:id", upload.none(), deleteFolder);
router.post("/create-folder", upload.none(), createFolder);
router.post("/create-file/:id", upload.single("file"), createFile);
router.get("/download-folder/:id", upload.none(), downloadFolder);

module.exports = router;
