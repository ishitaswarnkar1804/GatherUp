document.addEventListener("DOMContentLoaded", () => {

    const loader = document.querySelector(".loader");

    window.setTimeout(() => loader?.classList.add("hide"), 650);

    const navbar = document.querySelector(".navbar");

    const menu = document.querySelector(".menu");

    const mobileMenu = document.querySelector(".mobile-menu");

    const updateNav = () => navbar?.classList.toggle("scrolled", window.scrollY > 20);

    updateNav();

    window.addEventListener("scroll", updateNav, { passive: true });

    menu?.addEventListener("click", () => {

        const open = menu.classList.toggle("open");

        mobileMenu?.classList.toggle("open", open);

        menu.setAttribute("aria-expanded", String(open));

    });

    mobileMenu?.querySelectorAll("a").forEach(link => link.addEventListener("click", () => {

        menu?.classList.remove("open");

        mobileMenu?.classList.remove("open");

        menu?.setAttribute("aria-expanded", "false");

    }));

    document.querySelectorAll('a[href^="#"]').forEach(link => {

        link.addEventListener("click", e => {

            const target = document.querySelector(link.getAttribute("href"));

            if (!target) return;

            e.preventDefault();

            target.scrollIntoView({
                behavior: "smooth",
                block: "start"
            });

        });

    });

    const revealObserver = new IntersectionObserver(entries => {

        entries.forEach(entry => {

            if (entry.isIntersecting) {

                entry.target.classList.add("show");

                revealObserver.unobserve(entry.target);

            }

        });

    }, { threshold: 0.12 });

    document.querySelectorAll(".reveal").forEach(el => {
        revealObserver.observe(el);
    });


    const tabs = document.querySelectorAll(".tab");

    const panels = document.querySelectorAll(".stage-panel");

    tabs.forEach(tab => tab.addEventListener("click", () => {

        const key = tab.dataset.stage;

        tabs.forEach(t => t.classList.toggle("active", t === tab));

        panels.forEach(panel => {
            panel.classList.toggle("active", panel.dataset.panel === key);
        });

    }));


    document.querySelectorAll(".password-toggle").forEach(button => {

        button.addEventListener("click", () => {

            const input = document.getElementById(button.dataset.password);

            if (!input) return;

            const visible = input.type === "text";

            input.type = visible ? "password" : "text";

            button.textContent = visible ? "Show" : "Hide";

        });

    });


    const password = document.getElementById("regPassword");

    const strength = document.getElementById("strengthBar");

    password?.addEventListener("input", () => {

        if (!strength) return;

        const value = password.value;

        let score = 0;

        if (value.length >= 8) score++;

        if (/[A-Z]/.test(value)) score++;

        if (/[0-9]/.test(value)) score++;

        if (/[^A-Za-z0-9]/.test(value)) score++;

        strength.style.width = `${score * 25}%`;

    });


    const registerForm = document.getElementById("registerForm");

    registerForm?.addEventListener("submit", async e => {

        e.preventDefault();

        const button = registerForm.querySelector("button[type=submit]");

        if (!button) return;

        const original = button.innerHTML;

        const firstName = document.getElementById("firstName")?.value.trim();

        const lastName = document.getElementById("lastName")?.value.trim();

        const email = document.getElementById("regEmail")?.value.trim();

        const passwordValue = document.getElementById("regPassword")?.value;

        button.disabled = true;

        button.innerHTML = "Creating account…";

        try {

            const response = await fetch("/auth/register", {

                method: "POST",

                headers: {
                    "Content-Type": "application/json"
                },

                body: JSON.stringify({
                    first_name: firstName,
                    last_name: lastName,
                    email: email,
                    password: passwordValue
                })

            });

            const data = await response.json();

            if (!response.ok) {
                throw new Error(data.detail || "Registration failed");
            }

            button.innerHTML = "Account created ✓";

            setTimeout(() => {
                window.location.href = "/login";
            }, 500);

        } catch (error) {

            alert(error.message);

        } finally {

            button.disabled = false;

            button.innerHTML = original;

        }

    });


    const loginForm = document.getElementById("loginForm");

    loginForm?.addEventListener("submit", async e => {

        e.preventDefault();

        const button = loginForm.querySelector("button[type=submit]");

        if (!button) return;

        const original = button.innerHTML;

        const email = document.getElementById("loginEmail")?.value.trim();

        const passwordValue = document.getElementById("loginPassword")?.value;

        button.disabled = true;

        button.innerHTML = "Signing in…";

        try {

            const response = await fetch("/auth/login", {

                method: "POST",

                headers: {
                    "Content-Type": "application/json"
                },

                body: JSON.stringify({
                    email: email,
                    password: passwordValue
                })

            });

            const data = await response.json();

            if (!response.ok) {
                throw new Error(data.detail || "Login failed");
            }

            localStorage.setItem("gatherup_token", data.access_token);

            window.location.href = "/dashboard";

        } catch (error) {

            alert(error.message);

        } finally {

            button.disabled = false;

            button.innerHTML = original;

        }

    });


    const glow = document.querySelector(".cursor-glow");

    if (glow && matchMedia("(pointer:fine)").matches) {

        glow.style.opacity = "1";

        window.addEventListener("pointermove", e => {

            glow.style.left = `${e.clientX}px`;

            glow.style.top = `${e.clientY}px`;

        }, { passive: true });

    }


    const tilt = document.querySelector(".tilt");

    if (
        tilt &&
        matchMedia("(pointer:fine)").matches &&
        !matchMedia("(prefers-reduced-motion:reduce)").matches
    ) {

        const visual = tilt.closest(".hero-visual");

        visual?.addEventListener("pointermove", e => {

            const r = tilt.getBoundingClientRect();

            const x = (e.clientX - r.left) / r.width - 0.5;

            const y = (e.clientY - r.top) / r.height - 0.5;

            tilt.style.transform =
                `perspective(1100px) rotateY(${x * 4}deg) rotateX(${-y * 3}deg)`;

        });

        visual?.addEventListener("pointerleave", () => {
            tilt.style.transform = "";
        });

    }


    document.querySelectorAll(".magnetic").forEach(button => {

        if (!matchMedia("(pointer:fine)").matches) return;

        button.addEventListener("pointermove", e => {

            const r = button.getBoundingClientRect();

            const x = e.clientX - r.left - r.width / 2;

            const y = e.clientY - r.top - r.height / 2;

            button.style.transform =
                `translate(${x * 0.08}px,${y * 0.08}px)`;

        });

        button.addEventListener("pointerleave", () => {
            button.style.transform = "";
        });

    });

});


if ("serviceWorker" in navigator) {

    window.addEventListener("load", () => {

        navigator.serviceWorker
            .register("/service-worker.js")
            .catch(() => { });

    });

}