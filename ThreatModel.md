# Threatspec Project Threat Model

A threatspec project.


# Diagram
![Threat Model Diagram](ThreatModel.md.png)



# Exposures


# Acceptances


# Transfers


# Mitigations


# Reviews


# Connections

## External:Guest To CalcApp:Web:Server:Index
HTTP-GET

```
# @connects #guest to #index with HTTP-GET
@flaskapp.route('/')
def index_page():
    print(request.cookies)
    isUserLoggedIn = False


```
/home/kali/cyber/projects/Online_Calc/app/main.py:1

## External:Guest To CalcApp:Web:Server:Login
HTTP-GET

```
# @connects #guest to #login with HTTP-GET
@flaskapp.route('/login')
def login_page():
    return render_template('login.html')

def create_token(username, password):

```
/home/kali/cyber/projects/Online_Calc/app/main.py:1

## External:Guest To CalcApp:Web:Server:Logout
HTTP-GET

```
# @connects #guest to #logout with HTTP-GET
@flaskapp.route('/logout')
def logout_page():
    resp=make_response(redirect('/'))
    resp.delete_cookie('token')
    return resp

```
/home/kali/cyber/projects/Online_Calc/app/main.py:1

## External:Guest To CalcApp:Web:Server:Calculator
HTTP-GET

```
# @connects #guest to #calculator with HTTP-GET
@flaskapp.route('/calculator', methods = ['GET'])
def calculator_get():
    isUserLoggedIn = False

    if 'token' in request.cookies:

```
/home/kali/cyber/projects/Online_Calc/app/main.py:1

## External:Guest To CalcApp:Web:Server:Calculate
HTTP-POST

```
# @connects #guest to #calculate with HTTP-POST
@flaskapp.route('/calculate', methods = ['POST'])
def calculate_post():
    Number_1 = request.form.get('Number_1', type = int)
    Number_2 = request.form.get('Number_2', type = int)
    Operation = request.form.get('Operation')

```
/home/kali/cyber/projects/Online_Calc/app/main.py:1

## External:Guest To CalcApp:Web:Server:Calculate
HTTP-POST

```
# @connects #guest to #calculate with HTTP-POST
@flaskapp.route('/calculate2', methods = ['POST'])
def calculate_post2():
    Number_1 = request.form.get('Number_1', type = int)
    Number_2 = request.form.get('Number_2', type = int)
    Operation = request.form.get('Operation', type = str)

```
/home/kali/cyber/projects/Online_Calc/app/main.py:1

## CalcApp:VPC To CalcApp:VPC:WebServer
Network

```
# @connects #vpc to #subnet with Network
resource "aws_instance" "cyber94_jhiguita_calculator_2_webserver_tf" {
    ami = var.var_aws_ami_ubuntu_1804
    instance_type = "t2.micro"
    subnet_id = var.var_web_subnet_id
    count = 2

```
/home/kali/cyber/projects/Online_Calc/terraform-infra-modular/modules/webserver/main.tf:1


# Components

## External:Guest

## CalcApp:Web:Server:Index

## CalcApp:Web:Server:Login

## CalcApp:Web:Server:Logout

## CalcApp:Web:Server:Calculator

## CalcApp:Web:Server:Calculate

## CalcApp:VPC

## CalcApp:VPC:WebServer


# Threats


# Controls
