from flask import Flask, json, session, request
import tidalapi
import mysql.connector



api = Flask(__name__)
api.secret_key = b'_5#y2L"F4Q8z\n\xec]/'

@api.route('/authenticate', methods=['GET'])
def authenticate():
	conn = tidalapi.Session()
	conn.login_oauth_simple()
	data = {'tidal_session_id': conn.session_id, 'tidal_key': conn.access_token, 'tidal_token_type': conn.token_type }
	db = connect()
	cursor = db.cursor()
	cursor.execute("INSERT INTO tidalApi (session,tidal_key,type) VALUES (%s, %s, %s)", (conn.session_id, conn.access_token, conn.token_type))
	db.commit()
	return json.dumps(data)


@api.route('/tracks', methods=['GET'])
def get_tracks():
	conn = get_client()
	name = request.args.get('name')
	result = conn.search('track', name)
	tracks = []
	for track in result.tracks:
		tracks.append({
			'id': track.id,
			'name': track.name,
			'duration': track.duration,
			'artist': track.artist.name,
			'album': track.album.name,
			'image': track.album.image,
			'available': track.available
		})
	return json.dumps(tracks)


@api.route('/addTrack', methods=['GET'])
def add_track_to_favorite():
	conn = get_client()
	track_id = request.args.get('track')
	conn.user.favorites.add_track(track_id)
	track = conn.get_track(track_id)
	image = None
	if track.album is not None:
		image = track.album.image
	return json.dumps({
		'name': track.name,
		'trackId': track_id,
		'artist': track.artist.name,
		'image': image
	})



def get_client():
	db = connect()
	cursor = db.cursor()
	cursor.execute("SELECT * FROM tidalApi ORDER BY ID DESC LIMIT 1")
	data = cursor.fetchone()
	conn = tidalapi.Session()
	conn.load_oauth_session(data[1], data[3], data[2])
	return conn

def  connect():
	return mysql.connector.connect(
		user="root",
		password="root",
		host="mariadb",
		port=3306,
		database="rauschpflicht"
	)

if __name__ == '__main__':
	api.run(host='0.0.0.0', port=5222)
