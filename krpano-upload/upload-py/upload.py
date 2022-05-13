from flask import Flask, request, Response
import os
from os import path

app = Flask(__name__)  # 实例Flask应用
# 设置允许上传的文件格式
ALLOW_EXTENSIONS = ['png', 'jpg', 'jpeg']
# 设置图片保存文件夹
app.config['UPLOAD_FOLDER'] = r'C:\Program Files\Apache Software Foundation\Tomcat 10.0\webapps\krpano\server'
app.config['FILE_PATH'] = r''
app.config['IMG_PATH'] = r''
app.config['SERVER_PATH'] = r''
# 设置图片返回的域名前缀
image_url = "http://1.13.15.226:8000/image/"
# 设置图片压缩尺寸
image_c = 1000


# 跨域支持
def after_request(resp):
    resp.headers['Access-Control-Allow-Origin'] = '*'
    return resp


app.after_request(after_request)


# 判断文件后缀是否在列表中
def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[-1] in ALLOW_EXTENSIONS


# 心跳检测
@app.route("/", methods=["GET"])
def check():
    return 'Im live'


# 图片获取地址 用于存放静态文件
@app.route("/image/<imageId>")
def get_frame(imageId):
    # 图片上传保存的路径
    try:
        with open(r'C:\Program Files\Apache Software Foundation\Tomcat 10.0\webapps\krpano\server\{}'.format(imageId), 'rb') as f:
            image = f.read()
            result = Response(image, mimetype="image/jpg")
            return result
    except BaseException as e:
        return {"code": '503', "data": str(e), "message": "图片不存在"}

vr_path = ""
# 上传图片
@app.route("/upload_image", methods=['POST', "GET"])
def uploads():
    if request.method == 'POST':
        title = request.form['title']
        # author = request.form['author']
        # 获取文件
        uploaded_files = request.files.getlist('file')
        # 检测文件格式
        for file in uploaded_files:
            if file and allowed_file(file.filename):
                # 生成文件名
                file_name = file.filename
                # 保存原图
                file_path = app.config['UPLOAD_FOLDER']+"\\"+title
                os.makedirs(file_path, exist_ok=True)
                file.save(os.path.join(file_path, file_name))
                app.config['FILE_PATH'] = file_path
                app.config['SERVER_PATH'] = r'"http://1.13.15.226/krpano/server/' + title + '/' + 'vtour/tour.html"'
                # return {"code": '200', "image_url": image_url + file_name, "message": "成功"}

            else:
                return "格式错误，仅支持jpg、png、jpeg格式文件"
    return {"code": '503', "data": "", "message": "仅支持post方法"}


# 前端传递ID、图片到数据库，Python-Post接口
# 后端根据ID下载图片到暂存文件夹，赋值path
# 执行生成方法，服务存储至tomcat目录

@app.route('/create', methods=['get', 'post'])
def createVR():
    scaner_file(app.config['FILE_PATH'])
    tool = r'C:\krpano\MAKEVTOUR.bat'
    os.system('chcp 65001')
    os.system(tool + ' ' + app.config['IMG_PATH'])
    print(app.config['IMG_PATH'])
    return app.config['SERVER_PATH']


# 遍历文件夹下的所有文件
def scaner_file(url):
    app.config['IMG_PATH'] = ''
    # 遍历当前路径下所有文件
    file = os.listdir(url)
    for f in file:
        # 字符串拼接
        real_url = '"' + path.join(url, f) + '"'
        # 打印出来
        app.config['IMG_PATH'] = app.config['IMG_PATH'] + ' ' + real_url + ' '
        print(app.config['IMG_PATH'])




if __name__ == "__main__":
    app.run(host="0.0.0.0", port=8000, debug=True)  # 项目入口
