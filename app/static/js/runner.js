class GlossyTypewriter {
    constructor(el) {
        this.el = el;
        this.words = JSON.parse(el.dataset.words || "[]");
        this.typeSpeed = parseInt(el.dataset.typeSpeed || "90", 10);
        this.deleteSpeed = parseInt(el.dataset.deleteSpeed || "45", 10);
        this.pause = parseInt(el.dataset.pause || "1100", 10);

        // a persistent text node so the glossy pseudo-elements (which
        // read data-text) and the visible cursor can coexist
        this.textNode = document.createElement("span");
        this.textNode.className = "gt-text";
        this.el.insertBefore(this.textNode, this.el.firstChild);

        this.wordIndex = 0;
        this.charIndex = 0;
        this.reduced = window.matchMedia("(prefers-reduced-motion: reduce)").matches;
    }

    start() {
        if (!this.words.length) return;
        if (this.reduced) {
            this.render(this.words[this.words.length - 1]);
            return;
        }
        this.step();
    }

    render(text) {
        this.textNode.textContent = text;
        this.el.setAttribute("data-text", text);
    }

    step() {
        const word = this.words[this.wordIndex];
        const isLastWord = this.wordIndex === this.words.length - 1;

        this.charIndex++;
        this.render(word.slice(0, this.charIndex));

        if (this.charIndex < word.length) {
            setTimeout(() => this.step(), this.typeSpeed);
            return;
        }

        // finished typing this word
        if (isLastWord) {
            return; // stop here, cursor keeps blinking via CSS
        }
        setTimeout(() => this.deleteStep(), this.pause);
    }

    deleteStep() {
        const word = this.words[this.wordIndex];
        this.charIndex--;
        this.render(word.slice(0, this.charIndex));

        if (this.charIndex > 0) {
            setTimeout(() => this.deleteStep(), this.deleteSpeed);
            return;
        }

        this.wordIndex++;
        setTimeout(() => this.step(), this.typeSpeed);
    }
}

document.querySelectorAll(".glossy-typewriter").forEach((el) => {
    new GlossyTypewriter(el).start();
});