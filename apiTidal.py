from flask import Flask, json, session, request
import tidalapi

api = Flask(__name__)
api.secret_key = b'_5#y2L"F4Q8z\n\xec]/'

@api.route('/authenticate', methods=['GET'])
def get_authenticate():
	conn = tidalapi.Session()
	conn.login_oauth_simple()
	session['tidal_key'] = conn.access_token
	session['tidal_session_id'] = conn.session_id
	session['tidal_token_type'] = conn.token_type
	return json.dumps(session['tidal_session_id'])


@api.route('/tracks', methods=['GET'])
def get_tracks():
	conn = get_client()
	name = request.args.get('name')
	result = conn.search('track', name)
	tracks = {}
	index = 0
	for track in result.tracks:
		tracks[track.name] = {'duration': track.duration, 'artist': track.artist.name, 'album': track.album.name, 'available': track.available}
	return json.dumps(tracks)


def get_client():
	conn = tidalapi.Session()
	conn.load_oauth_session(session['tidal_session_id'], session['tidal_token_type'], session['tidal_key'])
	return conn

if __name__ == '__main__':
    api.run()