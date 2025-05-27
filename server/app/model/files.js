const mongoose = require('mongoose');
const Schema = mongoose.Schema;

const fileSchema = new Schema({
    name: {
        type: String,
        required: true,
        trim: true
    }, 
    file_name: {
        type: String,
        required: true,
        trim: true
    }, 
    date: {
        type: Date,
        default: Date.now
    }, 
    file_type: {
        type: String,
        required: true,
        trim: true
    }
}, { timestamps: true }); 

module.exports = mongoose.model('File', fileSchema);
