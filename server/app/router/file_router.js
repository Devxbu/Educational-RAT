const express = require("express");
const multer = require('multer');
const { uploadFile, downloadFile, deleteFile, listFiles, searchFile } = require("../controller/file_controller");

const router = express.Router();

const storage = multer.memoryStorage();
const upload = multer({ storage: storage });

router.post("/upload", upload.single('file'), uploadFile);
router.post("/download/:id", upload.single('file'), downloadFile);
router.delete("/delete/:id", upload.none(), deleteFile);
router.get("/list", upload.single('file'), listFiles);
router.get("/search", upload.single('file'), searchFile);

module.exports = router;
