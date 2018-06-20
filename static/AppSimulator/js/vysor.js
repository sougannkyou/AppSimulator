!function (e, t) {
    function n() {
        var e = {
            showSoftKeys: !0,
            pinTitleBar: !0,
            alwaysOnTop: !1,
            bitrate: 0,
            resolution: 0,
            decoder: 0,
            displaySettings: x[0],
            dimDisplay: !1
        };
        return e
    }

    function o(e) {
        return e ? (e.friendlyName && !e.friendlyName.length && delete e.friendlyName, e) : null
    }

    function i(e) {
        window.chrome && window.chrome.storage ? chrome.storage.local.get("device-settings", function (t) {
            e(t["device-settings"] || {})
        }) : e({})
    }

    function r(e, t) {
        e || (e = "web");
        var r = n();
        "inkwire" == e && (r.pinTitleBar = !1, r.showSoftKeys = !1), i(function (n) {
            t(o(n[e] || r))
        })
    }

    function s(e, t, n) {
        return o(t), window.chrome && window.chrome.storage && e && e.indexOf("127.0.0.1") == -1 ? void i(function (o) {
            o[e] = t, chrome.storage.local.set({"device-settings": o}, n)
        }) : void(n && n())
    }

    function c() {
        for (var e in x) {
            var t = x[e], n = new Option;
            $(n).html(t.name), $("#display-settings").append(n)
        }
    }

    function a(e) {
        $("#new-display-name").prop("value", e.friendlyName || null), $("#softkeys-check").prop("checked", !!e.showSoftKeys).change(), $("#pin-title-check").prop("checked", !!e.pinTitleBar).change(), $("#always-on-top-check").prop("checked", !!e.alwaysOnTop).change(), $("#bitrate").prop("selectedIndex", e.bitrate || 0), $("#decoder").prop("selectedIndex", e.decoder || 0), $("#resolution").prop("selectedIndex", e.resolution || 0);
        var t = e.displaySettings && e.displaySettings.name, n = 0;
        for (var o in x) {
            var i = x[o];
            if (i.name == t) {
                n = o;
                break
            }
        }
        $("#display-settings").prop("selectedIndex", n), $("#dim-display").prop("checked", !!e.dimDisplay)
    }

    function d(e) {
        chrome.storage.local.get(["whitelist", "serverMode"], function (t) {
            if (1 == t.serverMode) return void e("Any user can access this server.");
            if (2 == t.serverMode) return void e("Your Vysor Enterprise users can access this server.");
            var n;
            n = t.whitelist && "Array" == t.whitelist.constructor.name ? t.whitelist.length : 0, e(n + " user(s) can access this server.")
        })
    }

    function l(e) {
        for (var t = e.toString(16); t.length < 4;) t = "0" + t;
        return t
    }

    function u(e) {
        return unescape(encodeURIComponent(e))
    }

    function h(e) {
        return decodeURIComponent(escape(e))
    }

    function f(e) {
        return "ArrayBuffer" == e.constructor.name && (e = new Uint8Array(e)), h(String.fromCharCode.apply(null, e))
    }

    function m(e, t, n) {
        e = u(e);
        var o = e.length;
        n && o++, t || (t = new ArrayBuffer(o));
        var i = new Uint8Array(t);
        n && (i[e.length] = 0);
        for (var r = 0, s = e.length; r < s; r++) i[r] = e.charCodeAt(r);
        return t
    }

    function v(e, t) {
        function n(t) {
            o += f(t), e.read(n)
        }

        var o = "";
        e.onClose = function () {
            t(o)
        }, e.read(n)
    }

    function p(e) {
        var t = document.createElement("textarea");
        t.style.position = "fixed", t.style.top = 0, t.style.left = 0, t.style.width = "2em", t.style.height = "2em", t.style.padding = 0, t.style.border = "none", t.style.outline = "none", t.style.boxShadow = "none", t.style.background = "transparent", t.value = e, document.body.appendChild(t), t.select();
        try {
            document.execCommand("copy")
        } catch (e) {
            console.log("Oops, unable to copy")
        }
        document.body.removeChild(t)
    }

    function g() {
    }

    function y(e, t) {
        return window.chrome && window.chrome.identity ? void chrome.identity.getAuthToken({
            interactive: e,
            scopes: ["https://www.googleapis.com/auth/userinfo.profile", "https://www.googleapis.com/auth/userinfo.email", "https://www.googleapis.com/auth/chromewebstore.readonly"]
        }, function (e) {
            e || console.error("unable to get authToken", chrome.runtime.lastError), t(e)
        }) : (console.error("no auth token implemented"), void process.nextTick(t))
    }

    function b(e) {
        var t = $("#notificationModal"), n = t.find("#modal-ok"), o = t.find("#modal-cancel");
        n.unbind("click"), o.unbind("click"), t.unbind("hidden.bs.modal"), e.cancelButton = e.cancelButton || "Cancel", e.okButton = e.okButton || "OK", e.title = e.title || chrome.runtime.getManifest().name, e.body = e.body || "", e.hideCancel ? o.hide() : o.show(), n.text(e.okButton), o.text(e.cancelButton), t.find("#modal-title").text(e.title), t.find("#modal-body").html(e.body);
        var i;
        n.click(function () {
            i = !0, e.ok && e.ok() || $("#notificationModal").modal("hide")
        }), e.cancel && (t.on("hidden.bs.modal", function () {
            i || e.cancel()
        }), o.click(e.cancel)), $("#notificationModal").modal(), e.duration && setTimeout(function () {
            $("#notificationModal").modal("hide")
        }, e.duration)
    }

    function w(e, t) {
        b({title: e, body: t, duration: 8e3, hideCancel: !0})
    }

    function k(e) {
        if (e) {
            $("#whitelist-count").show(), d(function (t) {
                $("#whitelist-count a").text(t).click(function (t) {
                    chrome.app.window.create("whitelist.html", {
                        id: "whitelist",
                        innerBounds: {width: 768, height: 512, minWidth: 768, minHeight: 512}
                    }, function (t) {
                        t.onClosed.addListener(function () {
                            k(e)
                        })
                    })
                })
            }), $("#vysor-share-server-status").show(), $("#vysor-share-server-status").html('Vysor is sharing your devices: <a href="#">' + e + "</a>");
            var t = $("#vysor-share-server-status a");
            t.click(function () {
                p(e);
                var t = chrome.runtime.getManifest().name;
                w("Copied " + t + " Share Server URL to clipboard.", e)
            })
        } else $("#vysor-share-server-status").hide(), $("#whitelist-count").hide()
    }

    function S(e) {
        return $('.vysor-device[name="' + e + '"]')
    }

    function C(e, t) {
        var n = S(e);
        n && n.find(".friendly-name").text(t)
    }

    var x = [{name: "Default Settings", size: "reset", density: "reset"}, {
        name: "Resizable (96dpi)",
        size: "reset",
        density: "96",
        freeSize: !0
    }, {name: "Resizable (144dpi)", size: "reset", density: "144", freeSize: !0}, {
        name: "1080p (96dpi)",
        size: "1920x1080",
        density: "96"
    }, {name: "4K (144dpi)", size: "3840x2160", density: "144"}, {
        name: "Galaxy Nexus",
        size: "720x1280",
        density: "320"
    }, {name: "Nexus 4", size: "768x1280", density: "320"}, {
        name: "Nexus 5",
        size: "1080x1920",
        density: "480"
    }, {name: "Nexus 6", size: "1440x2560", density: "560"}, {
        name: "Nexus 6p",
        size: "1440x2560",
        density: "560"
    }, {name: "Nexus 7 (2012)", size: "800x1280", density: "213"}, {
        name: "Nexus 7 (2013)",
        size: "1200x1920",
        density: "320"
    }, {name: "Nexus 9", size: "1536x2048", density: "320"}];
    "\n".charCodeAt(0), (new Date).getTime();
    String.prototype.startsWith || Object.defineProperty(String.prototype, "startsWith", {
        enumerable: !1,
        configurable: !1,
        writable: !1,
        value: function (e, t) {
            return t = t || 0, this.lastIndexOf(e, t) === t
        }
    }), Object.fromArray = function (e) {
        var t = {};
        for (var n in e) {
            var o = e[n];
            t[o] = o
        }
        return t
    }, $.ajaxTransport("+binary", function (e, t, n) {
        if (window.FormData && (e.dataType && "binary" == e.dataType || e.data && (window.ArrayBuffer && e.data instanceof ArrayBuffer || window.Blob && e.data instanceof Blob))) return {
            send: function (t, n) {
                var o = new XMLHttpRequest, i = e.url, r = e.type, s = e.async || !0, c = e.responseType || "blob",
                    a = e.data || null, d = e.username || null, l = e.password || null;
                o.addEventListener("load", function () {
                    var t = {};
                    t[e.dataType] = o.response, n(o.status, o.statusText, t, o.getAllResponseHeaders())
                }), o.open(r, i, s, d, l);
                for (var u in t) o.setRequestHeader(u, t[u]);
                o.responseType = c, o.send(a)
            }, abort: function () {
                n.abort()
            }
        }
    });
    var A = function () {
        var e = {};
        return function (t, n) {
            if (e[t]) return void n(e[t]);
            var o = new XMLHttpRequest;
            o.open("GET", t, !0), o.responseType = "blob", o.onload = function (o) {
                n(e[t] = window.URL.createObjectURL(this.response))
            }, o.send()
        }
    }();
    !function () {
        function* e() {
        }

        var t = e();
        t.constructor.prototype.async = function () {
            function e() {
                i = o.throw(new Error(arguments)), n()
            }

            function t() {
                var e = arguments[0];
                i = o.next(e), n()
            }

            function n(n) {
                var r, s;
                if (!i.done) {
                    if (!i.value) return void(i = o.next(t));
                    if (i.value.constructor == Promise) return void i.value.then(t).catch(e);
                    if (i.value == Error) r = !0, i = o.next(e); else {
                        if (i.value != g) throw new Error("Unexpected yield value for callback. Only Error and Success allowed.");
                        s = !0, i = o.next(t)
                    }
                    if (!i.value) throw new Error("Double yield callbacks must explicitly define both Error and Success");
                    if (i.value == Error && r) throw new Error("Error callback already defined");
                    if (i.value == g && s) throw new Error("Success callback already defined");
                    if (i.value != Error && i.value != g) throw new Error("Unexpected yield value for callback. Only Error and Success allowed.");
                    i = r ? o.next(t) : o.next(e)
                }
            }

            var o = this, i = o.next();
            i.done || n()
        }
    }(), window.isElectron = function () {
        return navigator.userAgent.indexOf("Electron") != -1
    }, isElectron() || (window.sharedGlobals = window), function () {
        function e(e) {
            try {
                for (var t in e) e[t] && e[t].constructor != String && (e[t] = JSON.stringify(e[t]));
                i += e.join(" ") + "\n"
            } catch (e) {
            }
        }

        function t(e) {
            return new Promise(function (t, n) {
                return e.getConsoleLog ? void e.getConsoleLog(function (e) {
                    t({content: e && e.length ? e : "log is empty"})
                }) : void t("getConsoleLog not found")
            })
        }

        var n = console.log, o = console.error, i = "";
        console.error = function () {
            o.apply(console, arguments), e(Array.prototype.slice.call(arguments))
        }, console.log = function () {
            n.apply(console, arguments), e(Array.prototype.slice.call(arguments))
        }, sharedGlobals.getConsoleLog = function (e) {
            e(i)
        }, window.gistConsoleLog = function (e, n) {
            chrome.runtime.getBackgroundPage(function (o) {
                t(o).then(function (n) {
                    e["background.txt"] = n;
                    var o = chrome.app.window.getAll(), i = o.map(function (n) {
                        return t(n.contentWindow).then(function (t) {
                            e["window-" + n.id + ".txt"] = t
                        })
                    });
                    return Promise.all(i)
                }).then(function () {
                    var t = {description: chrome.runtime.getManifest().name + " console log", public: !1, files: e};
                    fetch("https://vysor.io/gist", {method: "POST", body: JSON.stringify(t)}).then(function (e) {
                        e.json().then(function (e) {
                            n(e.html_url)
                        })
                    })
                })
            })
        }
    }(), window.chrome && window.chrome.sockets && (chrome.sockets.tcp.onReceive.addListener(function (e) {
        var t = Socket.readers[e.socketId];
        null != t && t.dataReceived(new Uint8Array(e.data))
    }), chrome.sockets.tcp.onReceiveError.addListener(function (e) {
        var t = Socket.readers[e.socketId];
        null != t && (t.destroy(), t.dataReceived(null))
    }), chrome.sockets.tcpServer.onAccept.addListener(function (e) {
        chrome.sockets.tcp.setPaused(e.clientSocketId, !1);
        var t = Server.listeners[e.socketId];
        null != t && t(new Socket({socketId: e.clientSocketId}))
    })), function () {
        function e(t, n) {
            if (t.socketId) this.socketId = t.socketId, e.readers[this.socketId] = this; else if (window.chrome && window.chrome.sockets) chrome.sockets.tcp.create(function (o) {
                this.socketId = o.socketId, chrome.sockets.tcp.connect(this.socketId, t.host, t.port, function (t) {
                    t ? (chrome.runtime.lastError, this.destroy(), n(null)) : (e.readers[o.socketId] = this, n(this))
                }.bind(this))
            }.bind(this)); else {
                var o;
                t.ns ? (this.ns = t.ns, o = !0) : (this.ns = new require("net").Socket(), this.ns.connect({
                    port: t.port,
                    host: t.host
                }, function () {
                    o = !0, n(this)
                }.bind(this))), this.ns.on("close", function () {
                    this.destroy(), o || n(null)
                }.bind(this)), this.ns.on("data", function (e) {
                    this.dataReceived(e)
                }.bind(this))
            }
        }

        function t() {
        }

        e.readers = {}, e.connect = function (t, n) {
            return new e(t, n)
        }, e.pump = function (e, t, n) {
            if (!e || !t) return console.error("Socket.pump called with null socket", e, t), void n();
            var o = function () {
                e.read(i)
            }.bind(e), i = function (e) {
                var n = e.buffer;
                (e.byteOffset || e.length != n.byteLength) && (n = n.slice(e.byteOffset, e.byteOffset + e.length)), t.write(n, o)
            }.bind(t);
            e.read(i), e.onClose = n
        }, e.stream = function (t, n, o) {
            e.pump(t, n, function () {
                if (n && n.destroy(), o) {
                    var e = o;
                    o = null, e()
                }
            }), e.pump(n, t, function () {
                if (t && t.destroy(), o) {
                    var e = o;
                    o = null, e()
                }
            })
        }, e.eat = function (e) {
            function t() {
                e.read(t)
            }

            t()
        }, e.prototype.read = function () {
            if (this.pendingCallback) throw new Error("double callback");
            if (this.closed && !this.pending) {
                var e = this.onClose;
                return void(e && (delete this.onClose, e()))
            }
            var t = 0;
            "Number" == arguments[t].constructor.name ? this.pendingLength = arguments[t++] : this.pendingLength = 0;
            var e = arguments[t];
            if (!this.pending || this.paused) return void(this.pendingCallback = e);
            if (this.pendingLength) {
                if (this.pendingLength > this.buffered()) return void(this.pendingCallback = e)
            } else this.pendingLength = this.buffered();
            for (var n, o = 0; o < this.pendingLength;) {
                var i = this.pending.shift();
                this.bufferedLength -= i.length, this.pending.length || delete this.pending;
                var r = i, s = Math.min(r.byteLength, this.pendingLength - o);
                if (s != r.byteLength) {
                    var c = r.subarray(0, s), a = r.subarray(s);
                    this.unshift(a), r = c
                }
                n || r.byteLength == this.pendingLength || (n = new Uint8Array(this.pendingLength)), n ? n.set(r, o) : n = r, o += r.byteLength
            }
            e(n)
        }, e.prototype.write = function (e, t) {
            if (this.pendingWrite && console.error("write is already in progress!"), null == t && (console.error("write callback is null?"), t = function () {
            }), this.pendingWrite = t, window.chrome && window.chrome.sockets) chrome.sockets.tcp.send(this.socketId, e, function (n) {
                return chrome.runtime.lastError, !n || n.resultCode ? void delete this.pendingWrite : void(n.bytesSent < e.byteLength ? this.write(e.slice(n.bytesSent), t) : (delete this.pendingWrite, t()))
            }.bind(this)); else {
                if (!this.ns) return;
                if (!e.byteLength) return void require("process").nextTick(function () {
                    delete this.pendingWrite, t()
                }.bind(this));
                const n = window.Buffer || require("buffer").Buffer;
                this.ns.write(n.from(e), function () {
                    delete this.pendingWrite, t()
                }.bind(this))
            }
        }, e.prototype.destroy = function (e, t) {
            window.chrome && window.chrome.sockets ? chrome.sockets.tcp.close(this.socketId, function () {
                chrome.runtime.lastError
            }) : (this.dataReceived(null), this.ns && (this.ns.destroy(), delete this.ns))
        }, e.prototype.unshift = function (e) {
            0 != e.byteLength && (this.pending ? this.pending.unshift(e) : this.pending = [e], this.bufferedLength || (this.bufferedLength = 0), this.bufferedLength += e.length)
        }, e.prototype.dataReceived = function (e) {
            if (e && (e.asUint8Array && (e = e.asUint8Array()), e.constructor == ArrayBuffer && (e = new Uint8Array(e))), e && e.length) {
                var t = new Uint8Array(e);
                this.pending ? this.pending.push(t) : this.pending = [t]
            }
            if (null == e ? this.closed = !0 : (this.bufferedLength || (this.bufferedLength = 0), this.bufferedLength += e.length), this.paused || !this.pending || !this.pending.length) {
                var n = this.onClose;
                return void(this.closed && n && (delete this.onClose, n()))
            }
            var o = this.pendingLength, n = this.pendingCallback;
            n && (delete this.pendingCallback, this.read(o, n))
        }, e.prototype.buffered = function () {
            return this.bufferedLength
        }, e.prototype.pause = function () {
            this.paused || (this.paused = !0, this.onPause())
        }, e.prototype.resume = function () {
            this.paused && (this.paused = !1, this.onResume())
        }, e.prototype.onResume = function () {
            chrome.sockets.tcp.setPaused(this.socketId, !1, function () {
            })
        }, e.prototype.onPause = function () {
            chrome.sockets.tcp.setPaused(this.socketId, !0, function () {
            })
        }, t.listeners = {}, t.prototype.__proto__ = e.prototype, t.prototype.destroy = function () {
            window.chrome && window.chrome.sockets ? chrome.sockets.tcpServer.close(this.socketId, function () {
                chrome.runtime.lastError
            }) : this.ns && (this.ns.close(), delete this.ns)
        }, t.prototype.listen = function (n, o, i) {
            var r, s;
            "Number" == n.constructor.name ? (r = n, s = "0.0.0.0") : (s = n.address, r = n.port), window.chrome && window.chrome.sockets ? chrome.sockets.tcpServer.create(function (e) {
                this.socketId = e.socketId, t.listeners[this.socketId] = o, chrome.sockets.tcpServer.listen(e.socketId, s, r, function (e) {
                    return chrome.runtime.lastError, e ? (this.destroy(), void(i && i(e))) : void chrome.sockets.tcpServer.getInfo(this.socketId, function (t) {
                        this.localAddress = t.localAddress, this.localPort = t.localPort, i && i(e)
                    }.bind(this))
                }.bind(this))
            }.bind(this)) : (this.ns = require("net").createServer(function (t) {
                o(new e({ns: t}))
            }.bind(this)), this.ns.on("close", function () {
                this.destroy()
            }.bind(this)), this.ns.on("error", function (e) {
                i && i(e)
            }.bind(this)), this.ns.on("listening", function () {
                var e = this.ns.address();
                this.localAddress = e.address, this.localPort = e.port, i && i()
            }.bind(this)), this.ns.listen({port: r, host: s}))
        }, window.Socket = e, window.Server = t
    }(), function () {
        function e() {
        }

        var t = {};
        t.sendHostCommand = function (e, t) {
            Socket.connect({host: "127.0.0.1", port: 5037}, function (n) {
                if (!n) return void t();
                var o = e;
                e = l(e.length) + e, n.read(4, function (e) {
                    var i = f(e);
                    return "OKAY" != i ? (console.error("error in response to adb host command", o, i), n.destroy(), void t()) : void n.read(4, function (e) {
                        var o = f(e);
                        return e = parseInt(o, 16), 0 == e || "OKAY" == o ? void t(n, new ArrayBuffer(0)) : void n.read(e, function (e) {
                            t(n, e)
                        })
                    })
                }), n.write(m(e), function () {
                })
            })
        }, t.devices = function (e) {
            function n(e) {
                var t = e;
                e = e.replace("\t", " ");
                var n = e.indexOf(" ");
                if (n != -1) {
                    var i = e.substring(0, n);
                    e = e.substring(n).trim();
                    for (var r; r != e;) r = e, e = e.replace("  ", " ");
                    var s = {}, c = e.indexOf(" ");
                    c == -1 && (c = e.length);
                    var a = e.substring(0, c);
                    for (e = e.substring(c + 1); e.length && (n = e.indexOf(":"), n != -1);) {
                        var d, l = e.substring(0, n), u = e.substring(n + 1), h = u.indexOf(" "), f = u.indexOf(":");
                        if (h == -1 || f == -1) d = u, e = ""; else for (; h != -1 && h < f;) d = u.substring(0, h), e = u.substring(h + 1), h = u.indexOf(" ", h + 1);
                        s[l] = d
                    }
                    var m;
                    m = s.model ? s.model.replace("_", " ") : i, o[i] = {serialno: i, name: m, status: a, properties: t}
                }
            }

            var o = {};
            t.sendHostCommand("host:devices-l", function (t, i) {
                if (!t) return void e();
                t.destroy(), i = f(i), console.log("ADB devices:", i), i = i.trim();
                var r = i.split("\n");
                for (var s in r) s = r[s], n(s);
                console.log("parsed ADB devices:", o), e(o)
            })
        }, t.killServer = function (e) {
            t.sendHostCommand("host:kill-server", function (t, n) {
                return t ? (t.destroy(), n = f(n), void(e && e())) : void e()
            })
        }, t.sendClientCommand = function (e, t) {
            var n = e.command, o = e.serialno;
            Socket.connect({host: "127.0.0.1", port: 5037}, function (e) {
                if (!e) return void t();
                e.read(4, function (o) {
                    var i = f(o);
                    if ("OKAY" != i) return e.destroy(), void t(null);
                    var r = n;
                    r = l(r.length) + r, e.read(4, function (n) {
                        var o = f(n);
                        return "OKAY" != o ? (e.destroy(), void t(null)) : void t(e)
                    }), e.write(m(r), function () {
                    })
                });
                var i = "host:transport:" + o;
                i = l(i.length) + i, e.write(m(i), function () {
                })
            })
        }, t.shell = function (e, n) {
            var o = e.command;
            e.serialno;
            t.getOrCreateSockFactory(e).newSocket("shell:" + o, function (e) {
                return e ? void v(e, function (e) {
                    n(e)
                }) : void n()
            })
        }, t.forward = function (e, n) {
            var o = "host-serial:" + e.serialno + ":forward:" + e.from + ";" + e.to;
            t.sendHostCommand(o, function (e, t) {
                e && e.destroy(), n(e, t)
            })
        }, e.MKID = function (e, t, n, o) {
            return e.charCodeAt(0) | t.charCodeAt(0) << 8 | n.charCodeAt(0) << 16 | o.charCodeAt(0) << 24
        }, e.ID_RECV = e.MKID("R", "E", "C", "V"), e.ID_SEND = e.MKID("S", "E", "N", "D"), e.ID_DONE = e.MKID("D", "O", "N", "E"), e.ID_DATA = e.MKID("D", "A", "T", "A"), e.DATA_MAX = 65536, t.pull = function (n, o) {
            var i = n.file, r = (n.serialno, n.fileEntry), s = n.socket;
            s || !function () {
                var e;
                s = {
                    write: function (t, n) {
                        return e ? (e.onwriteend = n, void e.write(new Blob([t]))) : void r.createWriter(function (o) {
                            e = o, s.write(t, n)
                        })
                    }
                }
            }();
            var c = new DummySocket;
            Socket.pump(c, s, function () {
                o(r)
            }), t.getOrCreateSockFactory(n).newSocket("sync:", function (t) {
                function n(e) {
                    t.read(e, function (e) {
                        c.dataReceived(e), r()
                    })
                }

                function r() {
                    t.read(8, function (i) {
                        var r = new DataView(i.buffer, i.byteOffset, i.byteLength), s = r.getUint32(0, !0);
                        if (s == e.ID_DATA) {
                            var a = r.getUint32(4, !0);
                            return void n(a)
                        }
                        return t.destroy(), s == e.ID_DONE ? void c.dataReceived(null) : void o()
                    })
                }

                if (!t) return void o();
                var s = new ArrayBuffer(8), a = new DataView(s);
                a.setUint32(0, e.ID_RECV, !0), a.setUint32(4, i.length, !0), t.write(s, function () {
                    t.write(m(i), function () {
                        r()
                    })
                })
            })
        }, t.createSocketFactory = function (e) {
            return {
                newSocket: function (n, o) {
                    t.sendClientCommand({serialno: e, command: n}, o)
                }
            }
        }, t.getOrCreateSockFactory = function (e) {
            return e.socketFactory || t.createSocketFactory(e.serialno)
        }, t.push = function (n, o) {
            var i = n.file, r = (n.serialno, n.socket);
            t.getOrCreateSockFactory(n).newSocket("sync:", function (t) {
                if (!t) return void o();
                var n = new ArrayBuffer(8), s = new DataView(n), c = i + ",0644";
                s.setUint32(0, e.ID_SEND, !0), s.setUint32(4, c.length, !0), t.write(n, function () {
                    t.write(m(c), function () {
                        function n() {
                            r.read(function (t) {
                                if (t.byteLength > e.DATA_MAX) {
                                    var n = t.subarray(e.DATA_MAX);
                                    t = t.subarray(0, e.DATA_MAX), r.unshift(n)
                                }
                                i(t)
                            })
                        }

                        function i(o) {
                            var i = new ArrayBuffer(8), r = new DataView(i);
                            r.setUint32(0, e.ID_DATA, !0), r.setUint32(4, o.byteLength, !0), t.write(i, function () {
                                var e = o.buffer;
                                (o.byteOffset || o.length != e.byteLength) && (e = e.slice(o.byteOffset, o.byteOffset + o.byteLength)), t.write(e, function () {
                                    n()
                                })
                            })
                        }

                        r.onClose = function () {
                            var n = new ArrayBuffer(8), i = new DataView(n);
                            i.setUint32(0, e.ID_DONE, !0), i.setUint32(4, 0, !0), t.write(n, function () {
                                t.read(8, function () {
                                    o()
                                })
                            })
                        }, n()
                    })
                })
            })
        }, window.Adb = t
    }(), function () {
        function e() {
            chrome.usb.getUserSelectedDevices({
                multiple: !0,
                filters: [{interfaceClass: 255, interfaceSubclass: 66, interfaceProtocol: 1}]
            }, function (e) {
                $.each(e, function (e, t) {
                    var n = t.vendorId.toString(16) + ":" + t.productId.toString(16);
                    tracker.sendEvent("select-device", n), adbServer.refreshDevice(t, function (e) {
                        if (e) tracker.sendEvent("connect-device", e.properties["ro.product.name"], t.vendorId.toString(16) + ":" + t.productId.toString(16), n); else {
                            var o = chrome.runtime.getManifest().name;
                            chrome.notifications.create("reload", {
                                type: "basic",
                                iconUrl: "/icon.png",
                                title: o,
                                message: "An error occurred while connecting to the Android device. Restarting the Vysor app, or disconnecting and reconnecting the Android may resolve this issue.",
                                buttons: [{title: "Reload"}]
                            })
                        }
                    })
                })
            })
        }

        function t() {
            y(!1, function (e) {
                e ? ($("#login-container").hide(), chrome.identity.getProfileUserInfo(function (e) {
                    if (e) {
                        if ($("#login-info").show(), $("#login-email").text(e.email), $("#account-management").unbind("click"), !_lm._md || !_lm._md.managementUrl) return $("#account-management").text("Retrieve License."), $("#account-management-info").text("Unlicensed. Already purchased?"), void $("#account-management").click(function () {
                            chrome.storage.local.remove(["cachedLicense", "cachedClockworkLicense", "cachedEnterpriseLicense"], function () {
                                _lm.refresh(function (t) {
                                    t || b({
                                        hideCancel: !0,
                                        body: "No license found for account " + e.email + '. If this message was in error, please open an issue on the Support Forum.<br/><br/>Wrong account? <a href="https://plus.google.com/110558071969009568835/posts/5dWULG7ALmB" target="_blank">Read this</a>.'
                                    })
                                }, !0)
                            }.bind(this))
                        });
                        $("#account-management-info").text(""), $("#account-management").show(), $("#account-management").text(_lm._md.managementText), $("#account-management").attr("href", _lm._md.managementUrl)
                    }
                })) : $("#login-container").show()
            })
        }

        function o() {
            t(), _lm._il && ($("#purchase").hide(), $("#vysor-version").text("Vysor Pro Version " + chrome.runtime.getManifest().version), $(".navbar-brand").text("Vysor Pro"))
        }

        function i(e, t, n) {
            return function () {
                return _lm._il ? void t.apply(this, arguments) : (b({
                    title: "Vysor Pro",
                    body: "The " + e + " feature is only avaiable to Vysor Pro users.",
                    okButton: "Upgrade",
                    ok: function () {
                        _lm.startPurchase()
                    }
                }), void(n && n.apply(this, arguments)))
            }
        }

        function d(e, t) {
            var o = chrome.app.window.get(e);
            return o && o.contentWindow.showSettings ? (o.contentWindow.showSettings(), void o.show()) : void r(e, function (o) {
                function r() {
                    $("#settings-modal").modal("hide");
                    var n = $(u).prop("value");
                    o.friendlyName = n, C(e, o.friendlyName || t), s(e, o)
                }

                var c = $("#settings-ok"), d = $("#settings-cancel"), l = $("#settings-defaults"),
                    u = $("#new-display-name");
                u.prop("value", o.friendlyName), u.prop("placeholder", t), l.unbind("click"), c.unbind("click"), d.unbind("click"), $(u).unbind("focus"), $(u).unbind("keypress"), $(u).bind("keypress", function (e) {
                    var t = e.which;
                    if (13 == t) return r(), !1
                }), c.click(r), l.click(function () {
                    o = n(), a(o)
                });
                var h = t || friendlyName;
                $("#settings-title").text(h + " Settings"), $("#softkeys-check").unbind("change"), $("#pin-title-check").unbind("change"), $("#always-on-top-check").unbind("change"), $("#bitrate").unbind("change"), $("#resolution").unbind("change"), a(o), $("#softkeys-check").change(function () {
                    o.showSoftKeys = this.checked
                }), $("#pin-title-check").change(function () {
                    o.pinTitleBar = this.checked
                }), $("#always-on-top-check").change(i("Always On Top", function () {
                    o.alwaysOnTop = this.checked
                }, function () {
                    this.checked = !1
                })), $("#bitrate").change(i("Image Quality", function () {
                    o.bitrate = this.selectedIndex
                }, function () {
                    this.selectedIndex = 0
                })), $("#resolution").change(i("Image Quality", function () {
                    o.resolution = this.selectedIndex
                }, function () {
                    this.selectedIndex = 0
                })), $("#decoder").change(i("Image Quality", function () {
                    o.decoder = this.selectedIndex
                }, function () {
                    this.selectedIndex = 0
                })), $("#display-settings").change(i("Display Settings", function () {
                    var e = x[this.selectedIndex];
                    o.displaySettings = e
                }, function () {
                    this.selectedIndex = 0
                })), $("#dim-display").change(i("Dim Dislay", function () {
                    o.dimDisplay = this.checked
                }, function () {
                    this.checked = !1
                })), $("#settings-modal").modal()
            })
        }

        function l(e, t, n, o, s, c, a, l, f, v, g) {
            u = e, h = s, m = o, $("#share-all-check").prop("checked", l), Object.keys(e).length || !v ? $("#not-found").hide() : $("#not-found").show(), isElectron() || f && !v ? ($("#connect-android").hide(), $("#no-devices").show()) : ($("#connect-android").show(), $("#no-devices").hide()), f ? ($("#adb-server-status").show(), v ? $("#adb-server-status").text("Using built-in Vysor ADB.") : $("#adb-server-status").text("Using Android SDK ADB binary.")) : navigator.userAgent.indexOf("Windows NT 10") != -1 && null == g ? ($("#adb-server-status").show(), $("#adb-server-status").html("Windows 10 users MUST download the latest <a href='https://adb.clockworkmod.com' target='_blank'> Universal ADB Drivers</a>")) : ($("#adb-server-status").show(), $("#adb-server-status").text("ADB not running. Click Find Devices to get started."));
            var y = Object.keys(e), k = Object.keys(m);
            if ($.each($(".vysor-device"), function (t, n) {
                if (!e[n.name]) {
                    var o;
                    $.each(k, function (e, t) {
                        var i = m[t];
                        i.devices && i.devices[n.name] && (o = !0)
                    }), o || $(n).remove()
                }
            }), y.length) $("#no-vysor-devices").remove(), $("#choose-header").show(), $(y).each(function (n, o) {
                if (!t[o] || !t[o].farm) {
                    var s = e[o], l = s.name, f = $("#devices").find('.vysor-device[name="' + o + '"]');
                    if (!f.length) {
                        f = $('<a class="list-group-item vysor-device"><button type="button" class="btn btn-sm device-settings btn-default"><i class="fa fa-gear" title="Device Settings"></i></button><button type="button" class="btn btn-sm wireless btn-default"><i class="fa fa-wifi" title="Go Wireless"></i></button><button type="button" class="btn btn-sm share btn-default">Share</button><button type="button" class="btn btn-sm btn-success">View</button><img class="avatar img-rounded"></img><h5 class="list-group-item-heading friendly-name"></h5><p class="list-group-item-text serialno"></p></a>'), f[0].name = o;
                        var m = f.find(".share"), v = f.find("img");
                        v.click(function (e) {
                            e.stopPropagation();
                            var t = h[o].userInfo;
                            A(t.picture, function (e) {
                                w("Vysor Share", "Device in use by " + t.name)
                            })
                        }), f.find(".wireless").click(i("Go Wireless", function (e) {
                            e.stopPropagation(), startWireless(o)
                        }, function (e) {
                            e.stopPropagation()
                        })), t[o] ? ($(m).removeClass("btn-default").addClass("btn-danger"), m.text("Disconnect"), m.click(function (e) {
                            e.stopPropagation(), disconnectSharedDevice(o)
                        })) : ($(m).removeClass("btn-danger").addClass("btn-default"), m.click(i("Vysor Share", function (e) {
                            e.stopPropagation(), toggleShare(o, function (e, t) {
                                if (t) return void w("Vysor Share", t);
                                p(e);
                                chrome.runtime.getManifest().name;
                                w("Vysor Share", "Copied Vysor Share URL to clipboard");
                                var n = a[o];
                                n && closeWindow(n), closeWindow(o)
                            })
                        }, function (e) {
                            e.stopPropagation()
                        }))), $(f).find(".device-settings").click(function (e) {
                            e.stopPropagation(), d(o, l)
                        }), f.click(function () {
                            function e() {
                                tracker.sendEvent("click-device", l);
                                var e = a[o];
                                e && closeWindow(e), openWindow(o)
                            }

                            var t = u[o];
                            if ("unauthorized" == t.status) w(null, 'Check your Android device and accept the "Allow USB Debugging" prompt. You may need to disconnect and reconnect your Android for the dialog to show.'); else if ("offline" == t.status) w(null, "Your Android USB connection is offline. Please try rebooting your Android."); else {
                                if (h[o]) return void b({
                                    title: "Android In Use",
                                    body: "This Android is currently shared. Do you want to end the share session?",
                                    okButton: "Unshare and View",
                                    ok: function () {
                                        var t = a[o];
                                        t && unshareDevice(t), unshareDevice(o), e()
                                    }
                                });
                                e()
                            }
                        }), o.indexOf(":") != -1 ? f.find(".wireless").hide() : f.find(".wireless").show(), f.find(".serialno").text("Serial: " + o), $("#devices").append(f)
                    }
                    r(o, function (e) {
                        var t = e.friendlyName || l;
                        "unauthorized" == s.status && (t = "Unauthorized"), "offline" == s.status && (t = "Offline"), C(o, t)
                    });
                    var g = c[o];
                    g && e[g] ? f.hide() : f.show();
                    var m = f.find(".share"), v = f.find("img");
                    if (h[o] && h[o].userInfo && h[o].userInfo.picture) {
                        var y = h[o].userInfo;
                        v.attr("alt", "Device in use by " + y.name), A(y.picture, function (e) {
                            v.attr("src", e)
                        }), v.show()
                    } else v.hide();
                    t[o] || (h[o] ? m.text("Unshare") : m.text("Share"))
                }
            }); else {
                var S = $("#devices").find("#no-vysor-devices");
                S.length || (S = $('<a id="no-vysor-devices" href="https://plus.google.com/110558071969009568835/posts/Bb2wMXVwsQ7" target="_blank"><div class="alert alert-danger">No devices found. Make sure Android USB Debugging is enabled.</div></a>'), $("#devices").append(S)), f && !v || ($("#choose-header").hide(), S.hide())
            }
            $.each($(".vysor-farm"), function (e, t) {
                m[t.name] || $(t).remove()
            }), $(k).each(function (e, t) {
                var o = i;
                "117634581230601031713" == t && (o = function (e, t) {
                    return t
                });
                var s = m[t];
                if (s.devices) {
                    var c = Object.keys(s.devices);
                    if (c.length) {
                        var a = $("#farms-list").find("#farm-list-" + t);
                        if (!a.length) {
                            var l = $("<h5 class='list-header vysor-farm'>" + s.info.name + "'s Shared Devices <button class='btn btn-danger btn-xs' style='float: right;' type='button'>Disconnect</button></h5>");
                            l[0].name = t, $("#farms-list").append(l), l.find("button").click(function () {
                                destroyDeviceFarmConnection(t)
                            }), a = $("<div class='vysor-farm list-group'></div>"), a[0].name = t, a.attr("id", "farm-list-" + t), $("#farms-list").append(a)
                        }
                        $(c).each(function (e, i) {
                            function c(e) {
                                var o = m[t];
                                if (o.sharedDevices && o.sharedDevices[i] && o.sharedDevices[i].userInfo) {
                                    if (o.sharedDevices[i].userInfo.id == n.id) return void e();
                                    b({
                                        title: "Android In Use",
                                        body: "This Android is currently in use by " + o.sharedDevices[i].userInfo.name + " (" + o.sharedDevices[i].userInfo.email + "). Do you want to boot them off?",
                                        okButton: "Connect Anyways",
                                        ok: e
                                    })
                                } else e()
                            }

                            var l, u = s.devices[i], h = u.name;
                            l = s.gcmConn.gcmConns[i] ? "Serial: " + s.gcmConn.gcmConns[i].serialno : "Remote Serial: " + i;
                            var f = $("#farms-list").find('.vysor-device[name="' + i + '"]');
                            if (!f.length) {
                                f = $('<a class="list-group-item vysor-device"><button type="button" class="btn btn-sm device-settings btn-default"><i class="fa fa-gear" title="Device Settings"></i></button><button type="button" class="btn btn-sm connect"></button><button type="button" class="btn btn-sm btn-success">View</button><img class="avatar img-rounded"></img><h5 class="list-group-item-heading friendly-name"></h5><p class="list-group-item-text serialno"></p></a>'), f[0].name = i, f.find(".device-settings").click(function (e) {
                                    e.stopPropagation(), d(i, h)
                                }), f.find(".connect").click(o("Vysor Share", function (e) {
                                    var n = m[t];
                                    e.stopPropagation();
                                    var o = n.gcmConn.gcmConns[i];
                                    o ? (closeWindow(o.serialno), o.destroy(), f.find(".connect").text("Connect")) : c(function () {
                                        f.find(".connect").text("Disconnect"), createDeviceFarmConnection(t, i, function (e) {
                                            quietSerial(e)
                                        })
                                    })
                                }, function (e) {
                                    e.stopPropagation()
                                })), f.click(o("Vysor Share", function (e) {
                                    var n = m[t];
                                    c(function () {
                                        var e = n.gcmConn.gcmConns[i];
                                        e ? openWindow(e.serialno) : (f.find(".connect").text("Connect"), openWindow(i), createDeviceFarmConnection(t, i, function (e) {
                                            openWindow(e)
                                        }))
                                    })
                                }, function (e) {
                                    e.stopPropagation()
                                }));
                                var v = f.find("img");
                                v.click(function (e) {
                                    e.stopPropagation();
                                    var n = m[t], o = n.sharedDevices[i].userInfo;
                                    w("Vysor Share", "Device in use by " + o.name)
                                }), r(i, function (e) {
                                    e.friendlyName || h;
                                    C(i, e.friendlyName || h)
                                }), f.find(".serialno").text(l), a.append(f)
                            }
                            var v = f.find("img");
                            if (s.sharedDevices && s.sharedDevices[i] && s.sharedDevices[i].userInfo) {
                                var p = s.sharedDevices[i].userInfo;
                                v.attr("alt", "Device in use by " + p.name), A(p.picture, function (e) {
                                    v.attr("src", e)
                                }), v.show()
                            } else v.hide();
                            s.gcmConn.gcmConns[i] ? f.find(".connect").text("Disconnect").removeClass("btn-default").addClass("btn-danger") : f.find(".connect").text("Connect").removeClass("btn-danger").addClass("btn-default")
                        })
                    }
                }
            })
        }

        chrome.identity.onSignInChanged.addListener(function () {
            t()
        }), sharedGlobals._rl = o, $(document).ready(function () {
            function n() {
                chrome.storage.local.get(["vysorUsage"], function (e) {
                    var t = e.vysorUsage;
                    t || (t = 0);
                    var n = t / 36e5;
                    n = Math.round(2 * n) / 2, console.log("hours used", n), $("#used").html("You've used Vysor for " + n + " hours.<br/>An advertisement will be shown every 30 minutes while viewing an Android.<br/><br/>Purchase Vysor Pro to remove ads and unlock all features.")
                }), setTimeout(n, 36e5)
            }

            navigator.platform.toLowerCase().indexOf("win") == -1 && $("#windows").hide(), $("#vysor-keyboard-check").change(function () {
                chrome.storage.local.set({keyboard: this.checked}), updateKeyboard(this.checked)
            }), chrome.storage.local.get("keyboard", function (e) {
                $("#vysor-keyboard-check").prop("checked", e.keyboard)
            }), $("#customize-vysor").click(i("Customize Vysor", function () {
                chrome.app.window.create("customize.html", {
                    id: "customize",
                    innerBounds: {width: 768, height: 512, minWidth: 768, minHeight: 512}
                }, function (e) {
                    e.onClosed.addListener(function () {
                    })
                })
            })), $("#bugreport").click(function () {
                var e;
                b({
                    title: "Bug Report",
                    body: "Creating bug report. Please wait...",
                    okButton: "Cancel",
                    hideCancel: !0,
                    ok: function () {
                        e = !0
                    }
                }), gistConsoleLog({"adb-devices.json": {content: JSON.stringify(u, null, 2)}}, function (e) {
                    function t() {
                        b({
                            cancelButton: "OK",
                            okButton: "Copy Bug Report",
                            ok: function () {
                                $("#notificationModal").modal("hide"), p(e), setTimeout(t, 500)
                            },
                            title: "Bug Report",
                            body: 'Here is the <a href="' + e + '" target="_blank">link to your bug report</a>.<br/>Please copy the bug report link and submit it on the <a href="https://plus.google.com/110558071969009568835/posts/JLuG3yqRdSH" target="_blank">support forum</a>.'
                        })
                    }

                    t()
                })
            }), $("#logging-in").hide(),
                $("#login-info").hide(), $("#login-container").hide(), $("#connect-android").click(e), $("#vysor-version").text("Vysor Version " + chrome.runtime.getManifest().version), $("#reload-vysor").click(function () {
                chrome.runtime.reload()
            }), isElectron() ? ($("#desktop-app").hide(), $("#reset-vysor").click(function () {
                b({
                    title: "Reset Vysor",
                    body: "Resetting Vysor will log out the current user and clear all Vysor settings.",
                    okButton: "Reset",
                    ok: function () {
                        chrome.runtime.reset()
                    }
                })
            })) : $("#reset-vysor").hide(), $("#share-all-check").change(function () {
                chrome.storage.local.remove("lastDeviceFarmRegistrationId"), chrome.storage.local.set({"share-all-devices": this.checked}), this.checked ? startDeviceFarm(!0, function (e, t) {
                    if (t) return w("Vysor Share Server", t), void $("#share-all-check").prop("checked", !1);
                    k(e);
                    var n = chrome.runtime.getManifest().name;
                    w("Copied " + n + " Share Server URL to clipboard.", e), p(e)
                }) : stopDeviceFarm()
            }), chrome.storage.local.get("connect-automatically", function (e) {
                var t;
                t = e["connect-automatically"] === !1 ? 2 : e["connect-automatically"] === !0 ? 0 : e["connect-automatically"] || 1, $("#connect-automatically-select").prop("selectedIndex", t)
            }), $("#connect-automatically-select").change(function () {
                chrome.storage.local.set({"connect-automatically": this.selectedIndex})
            }), $("#connect-android").hide(), $(".purchase").click(function () {
                _lm.startPurchase()
            }), chrome.storage.local.get("lastConnectAddress", function (e) {
                e.lastConnectAddress && ($("#connect-address")[0].value = e.lastConnectAddress)
            }), $("#connect-ok").click(function () {
                $("#connectModal").modal("hide");
                var e = $("#connect-address")[0].value;
                chrome.storage.local.set({lastConnectAddress: e}), Adb.sendHostCommand("host:disconnect:" + e, function (t, n) {
                    t && t.destroy(), Adb.sendHostCommand("host:connect:" + e, function (e, t) {
                        e && console.log("adb connect result", f(t))
                    })
                })
            }), chrome.storage.local.get("survey0", function (e) {
                e.survey0 && $("#survey").hide()
            }), $("#survey").click(function () {
                chrome.storage.local.set({survey0: !0}), $("#survey").hide()
            }), $("#connect-cancel").click(function () {
                $("#connectModal").modal("hide")
            }), $("#connect-network").click(function () {
                $("#connectModal").modal()
            }), $("#login").click(function () {
                $("#login-line").hide(), $("#logging-in").show(), y(!0, function (e) {
                    return e ? ($("#logging-in").hide(), void t()) : (w(null, "Error retrieving auth token: " + chrome.runtime.lastError), $("#login-line").show(), void $("#logging-in").hide())
                })
            }), c(), o(), n(), window.tracker && tracker.sendAppView("list")
        });
        var u = {}, h = {}, m = {};
        chrome.notifications.onButtonClicked.addListener(function (e, t) {
            "never-start-automatically" == e ? $("#connect-automatically-select").prop("selectedIndex", 2) : e.startsWith("never-start-automatically-") && 1 == t && $("#connect-automatically-select").prop("selectedIndex", 2)
        }), sharedGlobals.refreshList = l
    }(), sharedGlobals.showModal = b, sharedGlobals.shortModal = w, sharedGlobals.updateVysorShareServer = k, sharedGlobals.findDeviceElement = S, sharedGlobals.updateDeviceName = C, t[""] = e
}({}, function () {
    return this
}());
