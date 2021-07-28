(function(window) {
    'use strict';

    function classReg(className) {
        return new RegExp("(^|\\s+)" + className + "(\\s+|$)")
    }
    var hasClass, addClass, removeClass;
    if ('classList' in document.documentElement) {
        hasClass = function(elem, c) {
            return elem.classList.contains(c)
        };
        addClass = function(elem, c) {
            elem.classList.add(c)
        };
        removeClass = function(elem, c) {
            elem.classList.remove(c)
        }
    } else {
        hasClass = function(elem, c) {
            return classReg(c).test(elem.className)
        };
        addClass = function(elem, c) {
            if (!hasClass(elem, c)) {
                elem.className = elem.className + ' ' + c
            }
        };
        removeClass = function(elem, c) {
            elem.className = elem.className.replace(classReg(c), ' ')
        }
    }

    function toggleClass(elem, c) {
        var fn = hasClass(elem, c) ? removeClass : addClass;
        fn(elem, c)
    }
    var classie = {
        hasClass: hasClass,
        addClass: addClass,
        removeClass: removeClass,
        toggleClass: toggleClass,
        has: hasClass,
        add: addClass,
        remove: removeClass,
        toggle: toggleClass
    };
    if (typeof define === 'function' && define.amd) {
        define(classie)
    } else {
        window.classie = classie
    }
})(window);
(function(window) {
    'use strict';

    function PathLoader(el) {
        this.el = el;
        this.el.style.strokeDasharray = this.el.style.strokeDashoffset = this.el.getTotalLength()
    }
    PathLoader.prototype._draw = function(val) {
        this.el.style.strokeDashoffset = this.el.getTotalLength() * (1 - val)
    }
    PathLoader.prototype.setProgress = function(val, callback) {
        this._draw(val);
        if (callback && typeof callback === 'function') {
            setTimeout(callback, 200)
        }
    }
    PathLoader.prototype.setProgressFn = function(fn) {
        if (typeof fn === 'function') {
            fn(this)
        }
    }
    window.PathLoader = PathLoader
})(window);
(function() {
    var $width = jQuery(this).width();
    if ($width > 1199) {
        var support = {
                animations: Modernizr.cssanimations
            },
            container = document.getElementById('body_wrapper'),
            header = container.querySelector('.ip-header'),
            loader = new PathLoader(document.getElementById('ip-loader-circle')),
            animEndEventNames = {
                'WebkitAnimation': 'webkitAnimationEnd',
                'OAnimation': 'oAnimationEnd',
                'msAnimation': 'MSAnimationEnd',
                'animation': 'animationend'
            },
            animEndEventName = animEndEventNames[Modernizr.prefixed('animation')];

        function init() {
            var onEndInitialAnimation = function() {
                if (support.animations) {
                    this.removeEventListener(animEndEventName, onEndInitialAnimation)
                }
                startLoading()
            };
            window.addEventListener('scroll', noscroll);
            classie.add(container, 'loading');
            if (support.animations) {
                container.addEventListener(animEndEventName, onEndInitialAnimation)
            } else {
                onEndInitialAnimation()
            }
        }

        function startLoading() {
            var simulationFn = function(instance) {
                var progress = 0,
                    interval = setInterval(function() {
                        progress = Math.min(progress + Math.random() * 0.1, 1);
                        instance.setProgress(progress);
                        if (progress === 1) {
                            classie.remove(container, 'loading');
                            classie.add(container, 'loaded');
                            clearInterval(interval);
                            var onEndHeaderAnimation = function(ev) {
                                if (support.animations) {
                                    if (ev.target !== header) return;
                                    this.removeEventListener(animEndEventName, onEndHeaderAnimation)
                                }
                                classie.add(document.body, 'layout-switch');
                                window.removeEventListener('scroll', noscroll)
                            };
                            if (support.animations) {
                                header.addEventListener(animEndEventName, onEndHeaderAnimation)
                            } else {
                                onEndHeaderAnimation()
                            }
                        }
                    }, 80)
            };
            loader.setProgressFn(simulationFn)
        }

        function noscroll() {
            window.scrollTo(0, 0)
        }
        init();
    }
})()