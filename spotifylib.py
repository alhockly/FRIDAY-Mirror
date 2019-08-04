from pyfy import Spotify


from pyfy import ClientCreds, Spotify
#

client_id ="2c0d0c49b20c4a2cbe346f42bb6dab74"
client_secret ="811e8611fafc4683b415caae2814d98b"
redirect_uri = 'http://localhost/'

username = "115937451"
scope = 'user-read-playback-state user-library-modify'


client = ClientCreds(client_id=client_id, client_secret=client_secret)
spt = Spotify(client_creds=client)
print(spt.auth_uri(client_id=client_id,scopes=scope.split(" "),redirect_uri=redirect_uri,show_dialog=True))
authcode=input().strip()

spt.build_user_creds(grant=authcode)