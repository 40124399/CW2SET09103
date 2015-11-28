
@app.route('/')
def download_file(filename):
    file_path = derive_filepath_from_filename(filename)
    file_handle = open(file_path, 'r')
    @after_this_request
    def remove_file(response):
        os.remove(file_path)
        return response
    return send_file(file_handle)
