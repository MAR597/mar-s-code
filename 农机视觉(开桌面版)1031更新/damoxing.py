import base64
import requests

API_KEY = "A5je7eqj6hVh8clcwetjiiQr"
SECRET_KEY = "mj9ppYQu1AF0D1XH9DHcrWI8WJXSNDN1"

def main():
    # 获取access token
    access_token = get_access_token()
    # 完整的API请求URL
    url = "https://aip.baidubce.com/rest/2.0/image-classify/v1/animal?access_token=" + access_token

    # 读取图像文件，并转换为base64编码的字符串
    with open("captured_photo.jpg", "rb") as image_file:
        # 将图像数据编码为base64字符串
        encoded_image = base64.b64encode(image_file.read())

    # 准备请求数据
    payload = {
        'image': encoded_image.decode('utf-8')  # 确保将bytes转换为str
    }

    headers = {
        'Content-Type': 'application/x-www-form-urlencoded',
        'Accept': 'application/json'
    }

    # 发送POST请求
    response = requests.post(url, data=payload, headers=headers)

    # 解析响应内容为JSON
    response_json = response.json()

    # 打印整个响应内容
    print(response_json)

    # 提取并打印动物分类结果
    if 'result' in response_json:
        for animal in response_json['result']:
            # 假设返回的数据中包含了动物的名称
            print(f"Animal: {animal['name']}, Probability: {animal['score']}")

def get_access_token():
    """
    使用 AK，SK 生成鉴权签名（Access Token）
    :return: access_token，或是None(如果错误)
    """
    url = "https://aip.baidubce.com/oauth/2.0/token"
    params = {
        "grant_type": "client_credentials",
        "client_id": API_KEY,
        "client_secret": SECRET_KEY
    }
    response = requests.post(url, params=params)
    return response.json().get("access_token")

if __name__ == '__main__':
    main()
