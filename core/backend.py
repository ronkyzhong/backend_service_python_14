from flask import Flask, request, jsonify, make_response
from flask_jwt_extended import JWTManager, create_access_token, jwt_required
from flask_restful import Resource, Api
from flask_sqlalchemy import SQLAlchemy
from jenkinsapi.jenkins import Jenkins

app = Flask(__name__)
# done: 输出中文
app.config["JSON_AS_ASCII"] = False

api = Api(app)
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+pymysql://python14:python14@stuq.ceshiren.com:23306/python14'
db = SQLAlchemy(app)
# token管理
app.config['JWT_SECRET_KEY'] = 'ceshiren.com'  # Change this!
jwt = JWTManager(app)

jenkins = Jenkins(
    'http://stuq.ceshiren.com:8020/',
    username='seveniruby',
    password='11743b5e008e546ec1e404933d00b35a07'
)


class User(db.Model):
    __tablename__ = "ronky_user"
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), unique=True, nullable=False)
    password = db.Column(db.String(80), unique=False, nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)

    def __repr__(self):
        return '<User %r>' % self.username


class TestCase(db.Model):
    __tablename__ = "ronky_testcase"
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(80), unique=True, nullable=False)
    description = db.Column(db.String(500), unique=False, nullable=False)
    data = db.Column(db.String(1024), unique=False, nullable=False)

    def __repr__(self):
        return '<TestCase %r>' % self.name

class Task(db.Model):
    __tablename__ = "ronky_task"
    id = db.Column(db.Integer, primary_key=True)
    task_name = db.Column(db.String(80), unique=True, nullable=False)
    status = db.Column(db.Integer, unique=True, nullable=False,default=0)

    def __repr__(self):
        return '<Task %r>' % self.name


class TestCaseApi(Resource):
    @jwt_required
    def get(self):
        r = []
        for t in TestCase.query.all():
            res = {}
            res['id'] = t.id
            res['name'] = t.name
            res['description'] = t.description
            res['data'] = t.data
            r.append(res)
        return r

    @jwt_required
    def post(self):
        t = TestCase(
            name=request.json['name'],
            description=request.json['description'],
            data=request.json['data']
        )
        db.session.add(t)
        db.session.commit()
        return {
            'msg': 'ok'
        }

    # done：更新用例
    @jwt_required
    def put(self, id):
        datas = request.get_json()
        get_test_case = TestCase.query.filter_by(id=id).first()
        if not get_test_case:
            print("没有此测试用例")
        if "name" in request.json and not isinstance(request.json['name'], str):
            print("测试用例名称 name 输入类型错误")
        if "description" in request.json and not isinstance(request.json['description'], str):
            print("测试用例描述 description 输入类型错误")
        if "data" in request.json and not isinstance(request.json['data'], str):
            print("测试用例描述 description 输入类型错误")

        if datas.get('name'):
            get_test_case.name = datas['name']
        if datas.get('description'):
            get_test_case.description = datas['description']
        if datas.get('data'):
            get_test_case.data = datas['data']
        db.session.add(get_test_case)
        db.session.commit()
        return {
            'msg': 'ok'
        }

    # done: 删除用例
    @jwt_required
    def delete(self, id):
        get_test_case = TestCase.query.filter_by(id=id).first()
        if not get_test_case:
            return {
                "errcode":0,
                "errmsg":"用例不存在不能进行删除"
            }
        db.session.delete(get_test_case)
        db.session.commit()
        return {"msg":"ok"}


class LoginApi(Resource):
    def get(self):
        User.query.all()
        return {'hello': 'world'}

    def post(self):
        # done: 查询数据库
        username = request.json.get('username', None)
        # todo: 通常密码不建议原文存储
        password = request.json.get('password', None)
        user = User.query.filter_by(username=username, password=password).first()
        # done：生成返回结构体
        if user is None:

            return jsonify(
                errcode=1,
                errmsg='用户名或者密码不对'
            )
        else:
            # done: 生成token
            return {
                'errcode': 0,
                'errmsg': 'ok',
                'username': user.username,
                'token': create_access_token(identity=user.username)
            }

class RegistryApi(Resource):
    def put(self):
        username = request.json.get('username', None)
        user = User.query.filter_by(username=username).first()
        if user:
            return jsonify(
                errcode=2,
                errmsg='用户名已经存在，请输入其他用户名进行注册'
            )
        email = request.json.get('email', None)
        user = User.query.filter_by(email=email).first()
        if user:
            return jsonify(
                errcode=2,
                errmsg='邮箱名已经存在，请输入其他邮箱进行注册'
            )
        password = request.json.get('password', None)
        new_user = User(
            username=request.json['username'],
            password=request.json['password'],
            email=request.json['email']
        )
        db.session.add(new_user)
        db.session.commit()
        return {
            'msg': 'ok'
        }


    # todo:注销
    def delete(self):
        pass


class TaskApi(Resource):
    # done: 查询所有的任务
    def get(self):
        task = Task.query.all()
        return {'task':task}

    def post(self):
        # todo: 用例获取
        testcases = request.json.get('testcases', None)
        # done: 调度jenkins
        jenkins['testcase'].invoke(
            securitytoken='11743b5e008e546ec1e404933d00b35a07',
            build_params={
                'testcases': testcases
            })

        return {
            'errcode': 0,
            'errmsg': 'ok'
        }

        # todo: 结果交给其他接口异步处理


class ReportApi(Resource):
    def get(self):
        # 展示报告数据和曲线图

        pass

    def post(self):
        # todo: pull模式 主动从jenkins中拉取数据
        jenkins['testcase'].get_last_build().get_resultset()
        # todo: push模式 让jenkins node主动push到服务器
        # todo: 把测试报告数据与测试报告文件保存
        pass


api.add_resource(TestCaseApi, '/testcase/<int:id>')
api.add_resource(LoginApi, '/login')
api.add_resource(TaskApi, '/task')
api.add_resource(RegistryApi, '/registry')


if __name__ == '__main__':
    app.run(debug=True)
