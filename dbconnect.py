import MySQLdb

def connection():
	conn = MySQLdb.connect(host='localhost', user='root', passwd='postgres', db='snapose')

	c = conn.cursor()

	return c, conn