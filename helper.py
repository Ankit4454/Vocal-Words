

help_str = """

<SwipeToDeleteItem>:
    size_hint_y: None
    height: content.height
        
    MDCardSwipeLayerBox:
        padding: "8dp"
            
        MDIconButton:
            icon: "trash-can"
            pos_hint: {"center_y": 0.5}
            on_release: app.remove_item(root)
                
    MDCardSwipeFrontBox:
        
        ThreeLineListItem:
            id: content
            text: root.text
            secondary_text: root.secondary_text
            tertiary_text: root.tertiary_text
            _no_ripple_effect: True

ScreenManager:
    LoginScreen:
    SignupScreen:
    WelcomeScreen:
    MailScreen:
    AnimScreen:

<LoginScreen>: 

    name:'loginscreen'  

    MDLabel:
        text: "Vocal Words"
        pos_hint:{'center_x':0.5,'center_y':0.8}
        halign: "center"
        font_style: "H4"


    MDTextField:
        id:login_email
        hint_text: "Email"
        icon_right: "email"
        icon_right_color: app.theme_cls.primary_color
        pos_hint:{'center_x': 0.5, 'center_y': 0.5}
        size_hint_x:None
        width:300
        helper_text: "Enter a valid email"
        helper_text_mode: "on_error"




    MDTextField:
        id:login_password
        hint_text: "Password"
        icon_right: "form-textbox-password"
        icon_right_color: app.theme_cls.primary_color
        pos_hint:{'center_x': 0.5, 'center_y': 0.4}
        size_hint_x:None
        width:300
        required: True
        helper_text_mode: "on_error"
        helper_text: "Enter Password"

    MDRoundFlatButton:
        text:"login"
        pos_hint:{'center_x': 0.5, 'center_y': 0.3}
        on_release:
            root.manager.current = 'animscreen'
            app.animate()
    
    MDTextButton:
        text: "Don't have an account? Sign Up"
        pos_hint: {'center_x':0.5,'center_y':0.2}
        on_press:
            root.manager.current = 'signupscreen'

<SignupScreen>:
    name: 'signupscreen'
    
    MDLabel:
        text: "Sign Up"
        pos_hint:{'center_x':0.5,'center_y':0.8}
        halign: "center"
        font_style: "H4"
    
    MDTextField:
        id: firstname
        hint_text: "First Name"
        pos_hint:{'center_x': 0.5, 'center_y': 0.7}
        size_hint_x:None
        width:300
        required: True
        helper_text_mode: "on_error"
        helper_text: "Required"

    MDTextField:
        id: lastname
        hint_text: "Last Name"
        pos_hint:{'center_x': 0.5, 'center_y': 0.6}
        size_hint_x:None
        width:300
        required: True
        helper_text_mode: "on_error"
        helper_text: "Required"
    
    MDTextField:
        id: email
        hint_text: "Email"
        pos_hint:{'center_x': 0.5, 'center_y': 0.5}
        size_hint_x:None
        width:300
        required: True
        helper_text_mode: "on_error"
        helper_text: "Required"
    
    MDTextField:
        id: password
        hint_text: "Password"
        pos_hint:{'center_x': 0.5, 'center_y': 0.4}
        size_hint_x:None
        width:300
        required: True
        helper_text_mode: "on_error"
        helper_text: "Required"
    
    MDRoundFlatButton:
        text:"Sign Up"
        pos_hint:{'center_x': 0.5, 'center_y': 0.3}
        on_release:
            app.signup()
            
    
    MDTextButton:
        text: "Already have an account? Sign In"
        pos_hint: {'center_x':0.5,'center_y':0.2}
        on_press:
            root.manager.current = 'loginscreen'
    
<WelcomeScreen>:
    name: 'welcomescreen'

    MDBottomNavigation:
        panel_color: .2, .2, .2, 1
        MDBottomNavigationItem:
            name: 'screen 1'
            text: 'Home'
            icon: 'home'
            
            MDToolbar:
                title: "Vocal Words"
                elevation: 10
                pos_hint: {'top':1.0}
                anchor_title: 'center'
            
            MDLabel:
                id:username_info
                font_style:'H5'
                halign:'center'      
            
            MDLabel:
                id:receiver_info
                font_style:'H6'
                halign: 'center'
                pos_hint:{'center_x': 0.5, 'center_y': 0.8} 
                
            MDLabel:
                id:subject_info
                font_style:'H6'
                halign: 'center'
                pos_hint:{'center_x': 0.5, 'center_y': 0.6}
            
            MDLabel:
                id:message_info
                font_style:'H6'
                halign: 'center'
                pos_hint:{'center_x': 0.5, 'center_y': 0.4}
            
            MDFloatingActionButton:
                icon: 'microphone'
                pos_hint:{'center_x': 0.5, 'center_y': 0.2}
                on_press:
                    app.get_email_info()
           
     

        MDBottomNavigationItem:
            name: 'screen 2'
            text: 'Profile'
            icon: 'account'
            
            FitImage:
                id: avatar
                pos_hint:{'center_x': 0.5, 'center_y': 0.8}
                size_hint: None,None
                size: "56dp","56dp"
                source: "profile.jpg"
                radius: [36,36,36,36,]
                            
            MDLabel:
                id: fullname 
                font_style: "Button"
                halign: 'center'
                pos_hint:{'center_x': 0.5, 'center_y': 0.7}
                        
            MDLabel:
                id: email_id
                font_style: "Caption"  
                halign: 'center' 
                pos_hint:{'center_x': 0.5, 'center_y': 0.65}
            
            
            MDList:
                pos_hint:{'center_x': 0.5, 'center_y': 0.5}
              
                OneLineIconListItem:
                    text: "Sent"
                    on_release:
                        root.manager.current = 'mailscreen'
                    
                    IconLeftWidget:
                        icon: 'email-send'                  
                
                OneLineIconListItem:
                    text: "Logout"
                    
                    IconLeftWidget:
                        icon: 'logout'





<MailScreen>:
    name: 'mailscreen'
    MDBoxLayout:
        orientation: "vertical"
        spacing: "8dp"
        
        MDToolbar:
            title: "SENT"
            elevation: 10
            pos_hint: {'top':1.0}
            left_action_items: [["arrow-left-thick", lambda x: app.back()]]
        
        ScrollView:
            MDList:
                id: md_list
                pos_hint: {'top':2.0}
                padding: 0


<AnimScreen>:
    name: 'animscreen'
    MDLabel:
        id: anim_info
        text: 'Loading'
        font_style:'H4'
        halign:'center' 




"""