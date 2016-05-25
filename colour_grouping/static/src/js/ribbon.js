/******************************************************************************
 Copyright (C) 2015 Akretion (http://www.akretion.com)
 @author Sylvain Calador <sylvain.calador@akretion.com>

 Copyright (C) 2016 Algi Open Source Solutions (http://www.algios.com)
 @author Javi Melendez <javi.melendez@algios.com>

 This program is free software: you can redistribute it and/or modify
 it under the terms of the GNU Affero General Public License as
 published by the Free Software Foundation, either version 3 of the
 License, or (at your option) any later version.

 This program is distributed in the hope that it will be useful,
 but WITHOUT ANY WARRANTY; without even the implied warranty of
 MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
 GNU Affero General Public License for more details.

 You should have received a copy of the GNU Affero General Public License
 along with this program.  If not, see <http://www.gnu.org/licenses/>.
 ******************************************************************************/

openerp.colour_grouping = function (instance) {

    var ribbon = $(document).find('.test-colour');
    var users = new instance.web.Model('res.users');
    var res = users.call('with_ribbon').then(
        function (with_ribbon) {
            if (with_ribbon) {
                ribbon.html('Negro');
                ribbon.show();
            } else {
                ribbon.hide();
            }
        }
    );

    var test = $(document).find('.test-env');
    var model = new instance.web.Model('ir.config_parameter');
    var res = model.call('get_param', ['ribbon.test']).then(
        function (value) {
            if (value != false) {
                test.html('T');
                test.show();
            }
        }
    );

/*
    // Get ribbon color from system parameters
    var res = model.call('get_param', ['ribbon.color']).then(
        function (strColor) {
            if (strColor && validStrColour(strColor)) {
                ribbon.css('color', strColor);
            }
        }
    );
*/
/*
    // Get ribbon background color from system parameters
    var res = model.call('get_param', ['ribbon.background.color']).then(
        function (strBackgroundColor) {
            if (strBackgroundColor && validStrColour(strBackgroundColor)) {
                ribbon.css('background-color', strBackgroundColor);
            }
        }
    );
*/
    // Code from: http://jsfiddle.net/WK_of_Angmar/xgA5C/
    function validStrColour(strToTest) {
        if (strToTest === "") {
            return false;
        }
        if (strToTest === "inherit") {
            return true;
        }
        if (strToTest === "transparent") {
            return true;
        }
        var image = document.createElement("img");
        image.style.color = "rgb(0, 0, 0)";
        image.style.color = strToTest;
        if (image.style.color !== "rgb(0, 0, 0)") {
            return true;
        }
        image.style.color = "rgb(255, 255, 255)";
        image.style.color = strToTest;
        return image.style.color !== "rgb(255, 255, 255)";
    }
}

