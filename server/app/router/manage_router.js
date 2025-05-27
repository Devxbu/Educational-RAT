const file_router = require('./file_router');
const folder_router = require('./folder_router');

module.exports = function(app){
    app.use('/api/file/', file_router);
    app.use('/api/folder/', folder_router);
}