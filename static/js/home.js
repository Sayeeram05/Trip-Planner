/* Home interactions: hero carousel, reveal animation, animated stats */
(function () {
    "use strict";

    function initHeroCarousel() {
        var carousel = document.getElementById("heroCarousel");
        if (!carousel) return;

        var slides = Array.prototype.slice.call(carousel.querySelectorAll(".hero-slide"));
        var dots = Array.prototype.slice.call(document.querySelectorAll(".hero-dot"));
        if (!slides.length) return;

        var currentIndex = 0;
        var intervalId = null;
        var delay = 5000;
        var touchStartX = 0;
        var touchStartY = 0;

        function setActive(index) {
            currentIndex = (index + slides.length) % slides.length;

            slides.forEach(function (slide, i) {
                var isActive = i === currentIndex;
                slide.classList.toggle("active", isActive);
                slide.setAttribute("aria-hidden", String(!isActive));
            });

            dots.forEach(function (dot, i) {
                var isActive = i === currentIndex;
                dot.classList.toggle("active", isActive);
                dot.setAttribute("aria-selected", String(isActive));
            });
        }

        function nextSlide() {
            setActive(currentIndex + 1);
        }

        function startAutoplay() {
            if (slides.length <= 1) return;
            stopAutoplay();
            intervalId = window.setInterval(nextSlide, delay);
        }

        function stopAutoplay() {
            if (intervalId) {
                window.clearInterval(intervalId);
                intervalId = null;
            }
        }

        dots.forEach(function (dot) {
            dot.addEventListener("click", function () {
                var index = Number(dot.getAttribute("data-slide"));
                setActive(index);
                startAutoplay();
            });
        });

        carousel.addEventListener("keydown", function (event) {
            if (event.key === "ArrowRight") {
                event.preventDefault();
                setActive(currentIndex + 1);
                startAutoplay();
            }
            if (event.key === "ArrowLeft") {
                event.preventDefault();
                setActive(currentIndex - 1);
                startAutoplay();
            }
        });

        carousel.addEventListener("touchstart", function (event) {
            if (!event.changedTouches || !event.changedTouches.length) return;
            touchStartX = event.changedTouches[0].clientX;
            touchStartY = event.changedTouches[0].clientY;
        }, { passive: true });

        carousel.addEventListener("touchend", function (event) {
            if (!event.changedTouches || !event.changedTouches.length) return;
            var deltaX = event.changedTouches[0].clientX - touchStartX;
            var deltaY = event.changedTouches[0].clientY - touchStartY;

            if (Math.abs(deltaX) < 42 || Math.abs(deltaX) < Math.abs(deltaY)) return;

            if (deltaX < 0) {
                setActive(currentIndex + 1);
            } else {
                setActive(currentIndex - 1);
            }
            startAutoplay();
        }, { passive: true });

        carousel.addEventListener("mouseenter", stopAutoplay);
        carousel.addEventListener("mouseleave", startAutoplay);
        carousel.addEventListener("focusin", stopAutoplay);
        carousel.addEventListener("focusout", startAutoplay);

        setActive(0);
        startAutoplay();
    }

    function initReveal() {
        var elements = document.querySelectorAll(".reveal");
        if (!elements.length) return;

        if (!("IntersectionObserver" in window)) {
            elements.forEach(function (el) { el.classList.add("revealed"); });
            return;
        }

        var observer = new IntersectionObserver(function (entries) {
            entries.forEach(function (entry) {
                if (entry.isIntersecting) {
                    entry.target.classList.add("revealed");
                    observer.unobserve(entry.target);
                }
            });
        }, {
            threshold: 0.16,
            rootMargin: "0px 0px -50px 0px"
        });

        elements.forEach(function (el) { observer.observe(el); });
    }

    function initCounters() {
        var counters = document.querySelectorAll("[data-count]");
        if (!counters.length) return;

        function runCounter(element) {
            var target = Number(element.getAttribute("data-count"));
            if (!target) return;

            var hasPercent = /%/.test(element.textContent || "");
            var hasPlus = /\+/.test(element.textContent || "");
            var startTime = null;
            var duration = 1300;

            function step(timestamp) {
                if (!startTime) startTime = timestamp;
                var progress = Math.min((timestamp - startTime) / duration, 1);
                var eased = 1 - Math.pow(1 - progress, 3);
                var value = Math.round(target * eased);
                element.textContent = String(value) + (hasPercent ? "%" : hasPlus ? "+" : "");
                if (progress < 1) window.requestAnimationFrame(step);
            }

            window.requestAnimationFrame(step);
        }

        if (!("IntersectionObserver" in window)) {
            counters.forEach(runCounter);
            return;
        }

        var observer = new IntersectionObserver(function (entries) {
            entries.forEach(function (entry) {
                if (entry.isIntersecting) {
                    runCounter(entry.target);
                    observer.unobserve(entry.target);
                }
            });
        }, { threshold: 0.55 });

        counters.forEach(function (counter) { observer.observe(counter); });
    }

    initHeroCarousel();
    initReveal();
    initCounters();
})();
