import asyncio
from pyppeteer import launch
from pyppeteer_stealth import stealth

url = 'https://www.wjx.cn/vj/mBpd0M3.aspx' # 问卷星的url，如果为vm，需要改成vj
num = 100

async def main():
    browser = await launch({
        # 路径就是你的谷歌浏览器的安装路径
        'executablePath': 'C:\\Program Files\\Google\\Chrome\\Application\\chrome.exe',
        'headless': False,
        'args': ['--no-sandbox', '--window-size=1366,850']
    })

    page = await browser.newPage()
    await page.setViewport({'width': 1366, 'height': 768})
    await stealth(page)

    await page.goto(url)
    await page.waitFor(1000)

    with open('wjx.js', 'r', encoding='utf-8') as f:
        script_content = f.read()

    await page.evaluate(script_content)

    submit = await page.querySelector('#submit_button')
    await submit.click()


    await page.waitFor(1000)
    verify_button = await page.querySelector('#SM_BTN_1')
    if verify_button:
        await verify_button.click()
        print("存在验证码")
        await page.waitFor(1000)
        await page.type('#captcha', '1234')
        await page.waitFor(5000)

    else:
        print("不存在验证码")

    await browser.close()

for i in range(num):
    asyncio.get_event_loop().run_until_complete(main())
    print("第{}次提交成功".format(i+1))
    asyncio.get_event_loop().run_until_complete(asyncio.sleep(5))
print("提交完成共{}次".format(num))
