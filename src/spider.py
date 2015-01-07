import cookielib, urllib2, re, time, math, binascii, hashlib
"""
MIT Licensed

Author: SecsAndCyber (matthewmolyett@gmail.com)
https://github.com/SecsAndCyber/py_gamerDNA

"""
SITE_ROOT = r"http://www.gamerdna.com/"

links = []

LINK_RE = re.compile('href\s*=\s*"(https?://[^"]+)"')

URL_BREAKDOWN = re.compile('https?://([^/]+)(/[^/?]+)*(.*)')
RUBY_BREAKDOWN = re.compile('https?://([^/]+)/([^?]+)(.*)')

class gamerDNA(object):
    def __init__(self, root, username, password ):
        self.cookies = cookielib.LWPCookieJar()
        handlers = [
            urllib2.HTTPHandler(),
            urllib2.HTTPSHandler(),
            urllib2.HTTPCookieProcessor(self.cookies)
            ]
        self.opener = urllib2.build_opener(*handlers)
    
        self.username = username
        self.password = password
    
        self.Root = root
                                  
    def Login( self ):
        login_url = SITE_ROOT + "login.php"
        data_block = "&".join ([
                                r"vb_login_username=%s" % ( self.username ),
                                "vb_login_password=",
                                "vb_login_password_help=Password",
                                "s=",
                                "do=login",
                                "vb_login_md5password=%s" % ( hashlib.md5(self.password).hexdigest() ),
                                "vb_login_md5password_utf=%s" % ( hashlib.md5(self.password).hexdigest() ),
                                ])
                
        page = self.opener.open(urllib2.Request( login_url, data_block ) )
        # On a login failure we get redirected to SITE_ROOT
        if login_url == page.geturl() and 200 == page.getcode():
            print page.info()
            
            page = self.opener.open(urllib2.Request( SITE_ROOT ) )
            if self.username in page.read():
                return True
        return False
        
    def Logout( self, redirect = SITE_ROOT ):
        page = self.opener.open(urllib2.Request( SITE_ROOT + "logout?r=%s" % (urllib2.quote(redirect)), "" ) )
        return redirect == page.geturl() and not (self.username in page.read())
        
    def SetLocation( self, location_string ):
        page = self.opener.open(urllib2.Request( SITE_ROOT + "rails/dna/update_location/?location=%s" % (urllib2.quote(location_string)), "" ) )
        return 200 == page.getcode()
        
    def CheckEmail( self, email ):
        page = self.opener.open(urllib2.Request( SITE_ROOT + "accounts/checkEmailUniquity.php?email=%s" % (urllib2.quote(email)), "" ) )
        return "\x20" == page.read()
        
    def AddGame( self, gid ):
        page = self.opener.open(urllib2.Request( SITE_ROOT + "dna/add_game/%d" % (gid), "" ) )
        return 200 == page.getcode()
        
    def RemoveGame( self, gid ):
        page = self.opener.open(urllib2.Request( SITE_ROOT + "dna/delete_game/%d" % (gid), "" ) )
        return 200 == page.getcode()
        
    def UpdateStatus( self, status ):
        data_block = "&".join (["new_quote=%s" % ( status )])
        page = self.opener.open(urllib2.Request( SITE_ROOT + "rails/profile/set_quote" , data_block ) )
        return 200 == page.getcode()
        
    def FollowGame( self, game_title ):
        page = self.opener.open(urllib2.Request( SITE_ROOT + "rails/game/follow/%s" % (game_title), "" ) )
        return 200 == page.getcode()
        
    def UnfollowGame( self, game_title ):
        page = self.opener.open(urllib2.Request( SITE_ROOT + "rails/game/unfollow/%s" % (game_title), "" ) )
        return 200 == page.getcode()
        
    def FollowUser( self, gamer_handle ):
        page = self.opener.open(urllib2.Request( SITE_ROOT + "rails/profile/follow/%s" % (gamer_handle), "" ) )
        return 200 == page.getcode()
        
    def UnfollowUser( self, gamer_handle ):
        page = self.opener.open(urllib2.Request( SITE_ROOT + "rails/profile/unfollow/%s" % (gamer_handle), "" ) )
        return 200 == page.getcode()
        
    def ReviewGame( self, gid, review ):
        data_block = "&".join (["_method=put","playing[Comment]=%s" % ( review )])
        page = self.opener.open(urllib2.Request( SITE_ROOT + "dna/game_update/%d" % (gid), data_block ) )
        return 200 == page.getcode()
        
    def SetBio( self, **kwargs):
        data_block = "&".join ([
            "user_profile[bio]=%s" %                            ( urllib2.quote(kwargs.get('bio',"Updated by bot"))),
            "user_profile[firstname]=%s" %                      ( urllib2.quote(kwargs.get('bio',"Super First Name"))),
            "user_profile[lastname]=%s" %                       ( urllib2.quote(kwargs.get('bio',"Mega Last Name"))),
            "user_profile[privacy_show_name]=%s" %              ( urllib2.quote(kwargs.get('bio',"1"))),
            "dob_month=%s" %                                    ( urllib2.quote(kwargs.get('bio',"2"))),
            "dob_day=%s" %                                      ( urllib2.quote(kwargs.get('bio',"2"))),
            "dob_year=%s" %                                     ( urllib2.quote(kwargs.get('bio',"1957"))),
            "user_profile[privacy_show_age]=%s" %               ( urllib2.quote(kwargs.get('show_age',"1"))),
            "gender=%s" %                                       ( urllib2.quote(kwargs.get('bio',"1"))),
            "user_profile[privacy_show_gender]=%s" %            ( urllib2.quote(kwargs.get('show_gender',"1"))),
            "user_profile[gamer_since]=%s" %                    ( urllib2.quote(kwargs.get('gamer_since',"1947"))),
            "user_profile[preferred_genre_id]=%s" %             ( urllib2.quote(kwargs.get('genre_id',"3"))),
            "user_profile[preferred_genre_description]=%s" %    ( urllib2.quote(kwargs.get('genre_description',"Scripting website access"))),
            "return_url=%s" %                                   ( urllib2.quote(kwargs.get('return_url', SITE_ROOT))),
        ])
        page = self.opener.open(urllib2.Request( SITE_ROOT + "rails/dna/save_info", data_block ) )
        return 200 == page.getcode()
    
    def PostImage( self, filename ):
        import requests
        url = SITE_ROOT + "rails/dna/image_submit"
        files = {'user_image[image]': open(filename, 'rb') }
        return requests.post( url, files=files, cookies=self.cookies, verify=False )
        
    def RemoveImage( self, image_id ):
        url = SITE_ROOT + "rails/dna/image_delete/%d" % ( image_id )
        page = self.opener.open(urllib2.Request( url, "" ) )
        return 200 == page.getcode()

        