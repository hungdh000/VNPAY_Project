odoo.define('vn_qrcode_facebook.form_widgets', function (require) {
"use strict";

var core = require('web.core');
var form_common = require('web.form_common');
var formats = require('web.formats');
var Model = require('web.Model');
var QWeb = core.qweb;

var WidgetOnButton = form_common.FormWidget.extend(form_common.ReinitializeWidgetMixin, {
    template : "facebook_share",
    events: {
        'click': function(event) {
                    var self = this;
                    event.preventDefault();
                    console.log('do event...');
                    var name = this.field_manager.get_field_value("name");
                    var list_price = this.field_manager.get_field_value("list_price");
                    var image = this.field_manager.get_field_value("image");
                    var description_sale = this.field_manager.get_field_value("description_sale");
                    if (!description_sale) {description_sale = "";}
                    var message = name +" - Price: " + list_price
                    console.log('message: ' + message)
                    // share product to facebook
                    FB.ui({
                        method: 'share',
                        display: 'popup',
                        title: message,
                        picture: self.photo_url,
                        description: description_sale,
                        href: 'vnpay.vn',
                        caption: 'VNPAY'
                    }, function(response) {
                      if (!response || response.error) {
                        console.log('Post not shared');

                      } else {
                        console.log('Post ID: ' + response.id);
                        alert("You shared facebook successful")
                      }
                    });

        },
    },

    init: function (view, code) {
        this._super(view, code);
        console.log('facebook share widget loading...');

        window.fbAsyncInit = function() {
            FB.init({
                appId: '170328833163620',
                status: true,
                cookie: true,
                xfbml: true,
                version: 'v2.7',
            });
        };

        (function(d, s, id){
          var js, fjs = d.getElementsByTagName(s)[0];
          if (d.getElementById(id)) {return;}
          js = d.createElement(s); js.id = id;
          js.src = "//connect.facebook.net/en_us/sdk.js";
          fjs.parentNode.insertBefore(js, fjs);
        }(document, 'script', 'facebook-jssdk'));
        console.log('facebook sdk loading...');
        var photo_url;
        this.field_manager.on("field_changed:name", this, function() {
            this.set({"name": this.field_manager.get_field_value("name")});
        });
        this.field_manager.on("field_changed:list_price", this,function() {
            this.set({"list_price": this.field_manager.get_field_value("list_price")});
        });
        this.field_manager.on("field_changed:image", this, function() {
            this.set({"image": this.field_manager.get_field_value("image")});
        });
        this.field_manager.on("field_changed:description_sale", this, function() {
            this.set({"description_sale": this.field_manager.get_field_value("description_sale")});
        });

    },

    start: function() {
        var self = this;
        //get image information on form
        var image = this.field_manager.get_field_value("image");
        // create form data to send to imgur
        var fd = new FormData();
        fd.append("image", image);
        var xhr = new XMLHttpRequest();
        xhr.open("POST", "https://api.imgur.com/3/image");
        xhr.setRequestHeader('Authorization', 'Client-ID '+ 'a99bb8d1259dab1');
        xhr.onload = function() {
            self.photo_url = JSON.parse(xhr.responseText).data.link;
            console.log('photo_url: ' + self.photo_url)
            }
        xhr.send(fd);
    },


});
// register unique widget, because Odoo does not know anything about it
core.form_custom_registry.add('facebook_share', WidgetOnButton);

});