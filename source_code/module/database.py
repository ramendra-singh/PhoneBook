import pymysql
import os
import file_util


class Database:
	def connect(self):
		user = os.environ['MYSQL_ROOT_USER']
		password = os.environ['MYSQL_ROOT_PASSWORD']
		db = os.environ['MYSQL_DATABASE']

		return pymysql.connect("db", user, password, db)

	def read(self, id):
		con = Database.connect(self)
		cursor = con.cursor()

		try:
			if id == None:
				cursor.execute("SELECT * FROM phone_book order by name asc")
			else:
				cursor.execute(
					"SELECT * FROM phone_book where id = %s order by name asc",
					(id,))

			return cursor.fetchall()
		except:
			return ()
		finally:
			con.close()

	def get_record(self, id):
		con = Database.connect(self)
		cursor = con.cursor()

		try:
			if id == None:
				cursor.execute("SELECT count(*) FROM phone_book")
			else:
				cursor.execute(
					"SELECT * FROM phone_book where id = %s order by name asc",
					(id,))

			rv1 = cursor.fetchall()
			d = {}
			d['data'] = rv1[0][0]
			return d
		except:
			return ()
		finally:
			con.close()

	def insert(self, data):
		con = Database.connect(self)
		cursor = con.cursor()

		try:
			counter = int(data['counter'])
			try:
				dummy_entry = data['dummy_entry']
				if dummy_entry:
					data['name'] = file_util.generate_random_string(count=5)
					data['address'] = file_util.generate_random_string(count=10)
					data['phone'] = file_util.generate_random_number(count=10)
			except:
				pass
			for i in range(counter):
				cursor.execute(
					"INSERT INTO phone_book(name,phone,address) VALUES(%s, %s, "
					"%s)",
					(data['name'], data['phone'], data['address'],))
				con.commit()

			return True
		except:
			con.rollback()

			return False
		finally:
			con.close()

	def update(self, id, data):
		con = Database.connect(self)
		cursor = con.cursor()

		try:
			cursor.execute(
				"UPDATE phone_book set name = %s, phone = %s, address = %s "
				"where id = %s",
				(data['name'], data['phone'], data['address'], id,))
			con.commit()

			return True
		except:
			con.rollback()

			return False
		finally:
			con.close()

	def delete(self, id):
		con = Database.connect(self)
		cursor = con.cursor()

		try:
			cursor.execute("DELETE FROM phone_book where id = %s", (id,))
			con.commit()

			return True
		except:
			con.rollback()

			return False
		finally:
			con.close()
