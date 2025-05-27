const mongoose = require('mongoose');
const Schema = mongoose.Schema;

const folderSchema = new Schema({
    name: {
        type: String,
        required: true,
        trim: true
    },
    parent: {
        type: Schema.Types.ObjectId,
        ref: 'Folder',
        default: null
    },
    files: [{
        type: Schema.Types.ObjectId,
        ref: 'File'
    }],
    folders: [{
        type: Schema.Types.ObjectId,
        ref: 'Folder'
    }]
}, { timestamps: true }); 

module.exports = mongoose.model('Folder', folderSchema);
