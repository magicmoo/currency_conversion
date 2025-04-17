from mcp.server.fastmcp import FastMCP
from enum import Enum
from bs4 import BeautifulSoup
import requests

mcp = FastMCP("currency_conversion")


def get_rate(src: str, tgt: str) -> float:
	url = 'https://themoneyconverter.com/zh-CN/{src}/{tgt}?amount=1.00'.format(src=src, tgt=tgt)
	resp = requests.get(url)
	soup = BeautifulSoup(resp.text, 'html.parser')
	exchange_rate = soup.find('output').text

	rate = exchange_rate.split('=')[1].strip().split(' ')[0]
	rate = float(rate)

	return rate

@mcp.tool()
async def conver(val: float, src: str, tgt: str) -> float:
	"""
	src和tgt均为币种的英文缩写
	该函数可以将数量为val的src币种转化为tgt币种并返回
	以下为常用币种的英文缩写
	JPY = '日元' KRW = '韩元' CNY = '人民币'
	EUR = '欧元' HKD = '港元' USD = '美元'
	"""

	rate = get_rate(src, tgt)

	return val * rate


if __name__ == "__main__":
	mcp.run()
	# conver('CNY', 'JPY')

