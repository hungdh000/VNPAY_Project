odoo.define('vn_qrcode_facebook.form_widgets', function (require) {
"use strict";

var core = require('web.core');
var form_common = require('web.form_common');
var formats = require('web.formats');
var Model = require('web.Model');
var QWeb = core.qweb;

var WidgetOnButton = form_common.FormWidget.extend(form_common.ReinitializeWidgetMixin, {
    template : "facebook_share_multi_product",
    events: {
        'click': function(event) {
                    event.preventDefault();
                    console.log('do event...');
                    var line_ids = this.field_manager.get_field_value("line_ids");
                    FB.login(function (response) {
                        if (response.authResponse) {
                            var access_token = FB.getAuthResponse()['accessToken'];
                            console.log('access_token: ' + access_token)
                            var is_post = 1
                            for (var i=0; i<line_ids.length; i++) {
                                var line_id = line_ids[i][1]
                                new Model("vn.social.network.line.wizard").query(['prod_name', 'prod_list_price', 'prod_image', 'prod_description'])
                                     .filter([['id', '=', line_id]])
                                     .first()
                                     .then(function (result) {
                                            console.log('result: '+ result);
                                            var name = result.prod_name;
                                            var list_price = result.prod_list_price;
                                            var image = result.prod_image;
                                            var description_sale = result.prod_description;
                                            if (!description_sale) {description_sale = "";}
                                            var message = name +"\n"+ list_price + "\n"+ description_sale
                                            // create form data to send to imgur
                                            var fd = new FormData();
                                            fd.append("image", image);
                                            var xhr = new XMLHttpRequest();
                                            xhr.open("POST", "https://api.imgur.com/3/image");
                                            //xhr.setRequestHeader('Authorization', 'Client-ID '+ 'a99bb8d1259dab1');
                                            xhr.setRequestHeader('Authorization', 'Client-ID '+ 'a8e3859d3aa45ae');
                                            xhr.onload = function() {
                                                var photo_url = JSON.parse(xhr.responseText).data.link;
                                                console.log('photo_url: ' + photo_url)
                                                FB.api("/me/photos", 'post',  {message: message, access_token: access_token, url: photo_url}, function(response) {
                                                  if (!response || response.error) {
                                                    console.log(response.error);
                                                    console.log('Error occured');
                                                    is_post = 0
                                                  } else {
                                                    console.log('Post ID: ' + response.id);
                                                    //alert("You shared facebook successful")
                                                  }
                                                });
                                            }
                                            xhr.send(fd);
                                    });
                            }
                            if (is_post) {
                                alert("You shared facebook successful")
                            }
                        } else {
                          console.log("Login attempt failed!");
                        }
                });




        },
    },

    init: function (view, code) {
        this._super(view, code);
        console.log('facebook share widget loading...');

        window.fbAsyncInit = function() {
                    FB.init({appId: '170328833163620',status: true, cookie: true,xfbml: true});
                };

        (function(d, s, id){
          var js, fjs = d.getElementsByTagName(s)[0];
          if (d.getElementById(id)) {return;}
          js = d.createElement(s); js.id = id;
          js.src = "//connect.facebook.net/en_US/all.js";
          fjs.parentNode.insertBefore(js, fjs);
        }(document, 'script', 'facebook-jssdk'));
        console.log('facebook sdk loading...');
        this.model_social_network_line = new Model("vn.social.network.line.wizard");
        this.field_manager.on("field_changed:line_ids", this, function() {
            this.set({"name": this.field_manager.get_field_value("line_ids")});
        });
    },

});
// register unique widget, because Odoo does not know anything about it
core.form_custom_registry.add('facebook_share_multi_product', WidgetOnButton);

});