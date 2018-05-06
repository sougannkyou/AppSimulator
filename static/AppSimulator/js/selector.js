function getNodeName(e) {
    e = e || window.event;
    var target = e.target || e.srcElement;
    return "";
}

function getParentA(e) {
    var href = "";
    var tagName = e.get(0).tagName;
    if (isNullOrEmpty(e) || isNullOrEmpty(tagName)) {
        return href;
    }

    href = e.attr("href");
    var parentE = e.parent();
    var pTagName = parentE.get(0).tagName;
    if (isNullOrEmpty(parentE) || isNullOrEmpty(pTagName) || pTagName.toLowerCase() === "body" || attr.substring(0, 5) === '[@id=') {
        return href;
    }
    return getParentA(parentE);
}

function getXPath(e, path) {
    var tagName = e.get(0).tagName;
    if (isNullOrEmpty(e) || isNullOrEmpty(tagName)) {
        return path;
    }
    var attr = getXPathAttr(e);
    tagName = tagName.toLowerCase() + attr;
    path = isNullOrEmpty(path) ? tagName : tagName + "/" + path;
    var parentE = e.parent();
    var pTagName = parentE.get(0).tagName;

    if (isNullOrEmpty(parentE) || isNullOrEmpty(pTagName) || pTagName.toLowerCase() === "body" || attr.substring(0, 5) === '[@id=') {
        return path;
    }
    return getXPath(parentE, path);
}

function getFullXPath(e, path) {
    var tagName = e.get(0).tagName;
    if (isNullOrEmpty(e) || isNullOrEmpty(tagName)) {
        return path;
    }
    var attr = getXPathAttr(e);

    tagName = tagName.toLowerCase() + attr;
    path = isNullOrEmpty(path) ? tagName : tagName + "/" + path;
    var parentE = e.parent();
    var pTagName = parentE.get(0).tagName;
    if (isNullOrEmpty(parentE) || isNullOrEmpty(pTagName) || pTagName.toLowerCase() === "html") {
        return '//' + path;
    }
    return getFullXPath(parentE, path);
}

function getClearJQSelector(e, path) {
    var tagName = e.get(0).tagName;
    if (isNullOrEmpty(e) || isNullOrEmpty(tagName)) {
        return path;
    }
    var expr = getJQSelectorAttr(e);
    if (expr.indexOf("#") !== -1) {
        tagName = tagName.toLowerCase() + expr;
    } else {
        tagName = tagName.toLowerCase();
    }
    path = isNullOrEmpty(path) ? tagName : tagName + " " + path;
    var parentE = e.parent();
    var pTagName = parentE.get(0).tagName;
    if (isNullOrEmpty(parentE) || isNullOrEmpty(pTagName) || pTagName.toLowerCase() === "body") {
        return path;
    }
    return getClearJQSelector(parentE, path);
}

function getJQSelector(e, path) {
    var hasId = false;
    var tagName = e.get(0).tagName;
    if (isNullOrEmpty(e) || isNullOrEmpty(tagName)) {
        return path;
    }
    var expr = getJQSelectorAttr(e);
    if (expr.indexOf("#") !== -1) {
        hasId = true;
    }
    tagName = tagName.toLowerCase() + expr;
    path = isNullOrEmpty(path) ? tagName : tagName + " > " + path;
    var parentE = e.parent();
    var pTagName = parentE.get(0).tagName;
    if (isNullOrEmpty(parentE) || hasId || isNullOrEmpty(pTagName) || pTagName.toLowerCase() === "body") {
        return path;
    }
    return getJQSelector(parentE, path);
}

function getCSSSelector(e, path) {
    var tagName = e.get(0).tagName;
    if (isNullOrEmpty(e) || isNullOrEmpty(tagName)) {
        return path;
    }
    var attr = getCSSAttr(e); //  #id or .css1.css2 or :nth-child(n)
    tagName = tagName.toLowerCase() + attr;
    path = isNullOrEmpty(path) ? tagName : tagName + " > " + path;
    var parentE = e.parent();
    var pTagName = parentE.get(0).tagName;
    if (isNullOrEmpty(parentE) || isNullOrEmpty(pTagName) || pTagName.toLowerCase() === "body" || attr.indexOf("#") === 0) {
        return path;
    }
    return getCSSSelector(parentE, path);
}

function getCSSAttr(e) {
    var id = e.attr('id');
    var cls = e.attr('class');
    var hasId = !isNullOrEmpty(id);
    var hasClass = !isNullOrEmpty(cls);
    var hasNum = e.siblings().length > 0;

    if (hasId) {
        return "#" + id; // #id
    } else if (hasNum) {
        var index = e.prevAll().length + 1; // bug注意："1"+"1" -> "11"
        return ":nth-child(" + index + ")"; // :nth-child(n)
    } else if (hasClass) {
        return "." + cls.trim().replace(/\s+/g, "\."); // .css1.css2.css3
    } else {
        return "";
    }
}

// normalize-space(@class) 并不解决class的先后顺序
// 'w650 pull-left' ->> [contains(@class,'w650') and contains(@class, 'pull-left')]
function convertClass(cls) {
    if (isNullOrEmpty(cls)) {
        return "";
    }

    var clear_cls = new Array();
    var ret = new Array();
    var CLS = cls.split(" ");
    for (var i = 0; i < CLS.length; i++) {
        if (!isNullOrEmpty(CLS[i])) {
            clear_cls.push(CLS[i]);
        }
    }

    if (clear_cls.length > 1) {
        for (var j = 0; j < clear_cls.length; j++) {
            ret.push("contains(@class,'" + clear_cls[j] + "')");
        }
        return "[" + ret.join(" and ") + "]"
    }

    return "[@class='" + cls + "']";
}

function getXPathAttr(e) {
    var tagName = e.get(0).tagName;
    var id = e.attr('id');
    var cls = e.attr('class');
    var new_cls = convertClass(cls); // 'w650 pull-left' ->> [contains(@class,'w650') and contains(@class, 'pull-left')]
    var hasId = !isNullOrEmpty(id);
    var hasClass = !isNullOrEmpty(cls);
    var hasNum = e.siblings(tagName).length > 0;

    if (hasId) {
        return "[@id='" + id + "']"; // [@id='id']
    } else if (hasNum) {
        var index = e.prevAll(tagName).length + 1;
        return '[' + index + ']'; // [n]
    } else if (hasClass) {
        return new_cls;
    } else {
        return '';
    }
}

function getJQSelectorAttr(e) {
    var tagName = e.get(0).tagName;
    var id = e.attr('id');
    var hasId = !isNullOrEmpty(id);
    if (hasId) { // #id
        id = "#" + id;
        return id;
    } else { // 获取xpath中的[n], n从0开始。
        if (e.siblings(tagName).length > 0) {
            var i = e.prevAll(tagName).length;
            return ':eq(' + i + ')';
        } else {
            return '';
        }
    }
}

function isNullOrEmpty(o) {
    return null === o || 'null' === o || '' === o || undefined === o || 'undefined' === o;
}

function Selector(e) { // 单击选取
    e = e || window.event;
    var target = e.target || e.srcElement;
    return $(target).getQuery();
}

function Selector2(e) { // 双击前进
    e = e || window.event;
    var target = e.target || e.srcElement;
    return $(target).getQuery2();
}


function getParentXPath(xpath) {
    // html/body/div[3]/div/div[1]/div[2]/div[3]/div[1]/div[@id='left-cont-wraper']/div[@id='f-d-w']/div[1]/div/div[2]/a[1]
    var l = xpath.split("\/");
    l.pop();
    parent = l.join("\/");
    return parent;
}

function getParentJQSelector(jqSelector) {
    var l = jqSelector.split(" ");
    l.pop();
    parent = l.join(" ");
    return parent;
}

function margeXPath(x1, x2) {
    if (isNullOrEmpty(x1) || isNullOrEmpty(x2)) {
        return isNullOrEmpty(x1) ? x2 : x1;
    } else {
        if (getLastTarget(x1) !== getLastTarget(x2)) {
            alert("不同类型的标签无法合并！");
            return x1;
        }

        var x = x1;
        var X1 = x1.split("/");
        var X2 = x2.split("/");
        var X = new Array();
        // //div[3]/div[2]/div[1]/div[2]/div[1]/div/div[2]/div[2]
        // //div[3]/div[2]/div[1]/div[2]/div[2]/div/div[2]/div[2]
        if (x1.replace(/\[.*?\]/g, "") === x2.replace(/\[.*?\]/g, "")) {
            for (var i = 0; i < X1.length; i++) {
                if (X1[i] === X2[i]) {
                    X.push(X1[i]);
                } else {
                    var same = X1[i].replace(/\[.*?\]/g, "");
                    X.push(same);
                }
            }
            return X.join("/");
        } else {
            // //div[contains(@class,'second2016_wrap') and contains(@class,'guoji_second_wrap')]/div[3]/div[4]/div[2]/div[1]/ul[contains(@class,'idx_cm_list') and contains(@class,'idx_cm_list_h')]/li/a
            // //div[contains(@class,'second2016_wrap') and contains(@class,'guoji_second_wrap')]/div[3]/div[3]/div[2]/ul/li[1]/a
            for (var j = 0; j < Math.min(X1.length, X2.length); j++) {
                if (X1[j] === X2[j]) {
                    X.push(X1[j]);
                } else {
                    break;
                }
            }
            if (X.join("/") === "/") {
                alert("合并范围过大，请重新选择");
                return x1;
            } else {
                console.log("margeXPath", x1, x2, X);
                return X.join("/") + "//" + getLastTarget(x1);
            }
        }
    }
}

function margeCSSSelector(c1, c2) {
    if (!isNullOrEmpty(c1) && !isNullOrEmpty(c2)) {
        var c = c1;
        var C1 = c1.split(" > ");
        var C2 = c2.split(" > ");
        var C = new Array();
        if (c1.replace(/\:nth-child\(\d+\)/g, "") === c2.replace(/\:nth-child\(\d+\)/g, "")) {
            for (var i = 0; i < C1.length; i++) {
                if (C1[i] === C2[i]) {
                    C.push(C1[i]);
                } else {
                    var same = C1[i].replace(/\:nth-child\(\d+\)/g, "");
                    C.push(same);
                }
            }
            return C.join(" > ");
        } else {
            for (var j = 0; j < Math.min(C1.length, C2.length); j++) {
                if (C1[j] === C2[j]) {
                    C.push(C1[j]);
                }
            }
            return C.join(" > ");
        }
    } else {
        return isNullOrEmpty(c1) ? c2 : c1;
    }
}

function xpath2selector(xpath) {
    var n = new Array();
    var l = xpath.split("/");
    var patt = /[\d+]/;
    for (var i = 0; i < l.length; i++) {
        var css = "";
        var attr = l[i].trim();
        if (attr !== "" && attr.indexOf("\[@") !== -1) {
            if (attr.indexOf("class=") !== -1) {   // class
                console.log("[xpath] attr", attr);
                css = attr.replace('\[\@class=\'', '\.').replace('\'\]', '').replace(/\s+/g, "\.");
            } else { // id
                css = attr.replace('\[\@id=\'', '#').replace('\'\]', '');
            }
        } else if (attr !== "" && patt.test(attr)) { // [index]
            // div[2] -> div:nth-child(3)
            var index = parseInt(attr.match(/[(\d+)]/g)[0]);
            index++;
            css = attr.replace('\[', '\:nth-child\(').replace('\]', '\)').replace(/\d+/, index);
        } else {
            css = attr;
        }
        n.push(css);
    }
    return n.join(" ").trim();
}

function getLastTarget(xpath) {
    var l = xpath.split("/");
    var s = l[l.length - 1];
    return s.replace(/\[.*\]/g, "");
}

function getClosestA(xpath) {
    var s = [];
    var l = xpath.split("/");
    for (var i = 0; i < l.length; i++) {
        s.push(l[i]);
        if (l[i].replace(/\[.*\]/g, "") === 'a') {
            break;
        }
    }
    return s.join("/");
}

function debugXPath(xpath) {
    if (isNullOrEmpty(xpath)) {
        return
    }
    var myFrame = document.getElementById("html").contentDocument;
    var results = myFrame.evaluate(xpath, myFrame, null, XPathResult.ORDERED_NODE_SNAPSHOT_TYPE, null);
    console.log("[xpath] evaluteXpath results:", results);
    var elements = [];
    for (var i = 0, l = results.snapshotLength; i < l; i++) {
        var element = results.snapshotItem(i);
        var rawClass = element.hasAttribute('class') && element.className;
        //element.className += " chromeXpathFinder";
        element.style.border = '2px dashed red';

        var elementDescription = '<' + element.tagName;
        for (var j = 0, m = element.attributes.length; j < m; j++) {
            var attr = element.attributes[j];
            var name = attr.name, value = attr.value;

            if (attr.name === 'class') {
                if (rawClass !== false) {
                    elementDescription += ' ' + name + '="' + rawClass + '"';
                }
            } else {
                elementDescription += ' ' + name + '="' + value + '"';
            }
        }
        elementDescription += '></' + element.tagName + '>';

        elements.push(elementDescription.toLowerCase());
    }
}

function matchXPath(xpath, attr, style) {
    if (isNullOrEmpty(xpath)) {
        return;
    }
    var myFrame = document.getElementById("html").contentDocument;
    var results = myFrame.evaluate(xpath, myFrame, null, XPathResult.ORDERED_NODE_SNAPSHOT_TYPE, null);
    for (var i = 0, l = results.snapshotLength; i < l; i++) {
        var e = results.snapshotItem(i);
        $(e).css(attr, style).css('opacity', 0.65);
    }
}

function getXPathText(xpath) {
    var ret = "";
    if (isNullOrEmpty(xpath)) {
        return ret;
    }
    var myFrame = document.getElementById("html").contentDocument;
    var results = myFrame.evaluate(xpath, myFrame, null, XPathResult.ORDERED_NODE_SNAPSHOT_TYPE, null);
    for (var i = 0, l = results.snapshotLength; i < l; i++) {
        var element = results.snapshotItem(i);
        ret += element.textContent.replace(/^\s+|\s+$/gm,'') + "\n";
    }
    return ret;
}