// 1. Back to Top Button Logic
const toTop = document.getElementById('toTop');
if (toTop) {
  window.addEventListener('scroll', () => {
    toTop.classList.toggle('visible', window.scrollY > 420);
  });
  toTop.addEventListener('click', () => {
    window.scrollTo({ top: 0, behavior: 'smooth' });
  });
}

// 2. Achievements Counter Animation Logic
const counters = [...document.querySelectorAll('[data-count]')];
let counted = false;

function animateCounters() {
  if (counted || counters.length === 0) return;
  const section = document.querySelector('.achievements');
  if (!section) return;
  const rect = section.getBoundingClientRect();
  if (rect.top > window.innerHeight * 0.75) return;
  counted = true;

  counters.forEach(counter => {
    const target = Number(counter.dataset.count);
    const duration = 1400;
    const start = performance.now();

    function tick(now) {
      const progress = Math.min((now - start) / duration, 1);
      const eased = 1 - Math.pow(1 - progress, 3);
      counter.textContent = Math.round(target * eased).toLocaleString('en-IN');
      if (progress < 1) requestAnimationFrame(tick);
    }
    requestAnimationFrame(tick);
  });
}
window.addEventListener('scroll', animateCounters);
document.addEventListener("DOMContentLoaded", animateCounters);


// 3. Global Slider Index Position Track Engine (BULLETPROOF VERSION)
let trackIndex = 0;

window.updateCarouselPosition = function() {
    const track = document.getElementById("carouselTrack");
    const cards = document.querySelectorAll(".carousel-card-node");
    
    if (!track || cards.length === 0) return;
    
    const cardWidth = cards[0].getBoundingClientRect().width;
    const gap = 20; 
    
    const totalMove = trackIndex * (cardWidth + gap);
    track.style.transform = `translateX(-${totalMove}px)`;
};

window.moveCarouselRight = function() {
    const cards = document.querySelectorAll(".carousel-card-node");
    if (cards.length === 0) return;
    
    if (trackIndex < cards.length - 3) {
        trackIndex++;
    } else {
        trackIndex = 0; 
    }
    window.updateCarouselPosition();
};

window.moveCarouselLeft = function() {
    if (trackIndex > 0) {
        trackIndex--;
        window.updateCarouselPosition();
    }
};

// Fire calculations securely after all components are ready
window.addEventListener("load", () => {
    window.updateCarouselPosition();
    setInterval(window.moveCarouselRight, 4000); // Autoplay every 4 seconds
});
window.addEventListener("resize", window.updateCarouselPosition);

let selectedLanguage = "english";
let lastCachedAnswer = "";
let botOpen = false;
let isMaximized = false;

// 🌟 FIX MARKDOWN FORMATTING SYSTEM MANUALLY
function parseMarkdownToHTML(text) {
    if(!text) return "";
    // Matches **bold text** securely and converts to raw HTML tags
    let formattedText = text.replace(/\*\*(.*?)\*\*/g, '<strong>$1</strong>');
    // Matches bullet points
    formattedText = formattedText.replace(/• /g, '• ');
    return formattedText;
}

window.toggleMaximizeChat = function() {
    const widget = document.getElementById("chatWidget");
    if (!widget) return;
    isMaximized = !isMaximized;
    if (isMaximized) {
        widget.classList.add("maximized-mode");
    } else {
        widget.classList.remove("maximized-mode");
    }
    setTimeout(window.updateCarouselPosition, 150); // Keep carousel synced if open behind
};

window.toggleChatWindow = function() {
    const widget = document.getElementById("chatWidget");
    const promptBubble = document.getElementById("botPromptBubble");
    botOpen = !botOpen;
    widget.style.display = botOpen ? "flex" : "none";
    if (promptBubble) {
        promptBubble.style.display = botOpen ? "none" : "flex";
    }
    if(botOpen && document.getElementById("chatWindow").children.length === 0) {
        triggerLanguageInitialization();
    }
};

window.catchBotEnter = function(e) { if(e.key === "Enter") sendDirectBotText(); };

async function postBotData(action, payload = {}) {
    payload.action = action;
    payload.lang = selectedLanguage;
    const res = await fetch('/get_bot_flow', {
        method: 'POST',
        headers: {'Content-Type': 'application/json'},
        body: JSON.stringify(payload)
    });
    return await res.json();
}

function pushBotTextBubble(text, sender) {
    const win = document.getElementById("chatWindow");
    const d = document.createElement("div");
    d.className = `message-bubble-wrapper ${sender === 'bot' ? 'system-bot-bubble' : 'active-user-bubble'}`;
    d.innerHTML = parseMarkdownToHTML(text); // Use the custom markdown converter
    win.appendChild(d);
    win.scrollTop = win.scrollHeight;
}

async function triggerLanguageInitialization() {
    const data = await postBotData("init_languages");
    pushBotTextBubble(data.text, "bot");
    renderOptionButtons(data.options, "lang_select");
}

function renderOptionButtons(options, mode) {
    const win = document.getElementById("chatWindow");
    const optGrp = document.createElement("div");
    optGrp.className = "interactive-options-stack";
    
    options.forEach(opt => {
        const b = document.createElement("button");
        b.className = "action-option-node";
        b.innerText = opt;
        if(mode === "lang_select") {
            b.onclick = () => handleLanguageSelection(opt);
        } else if(mode === "menu_select") {
            b.onclick = () => handleMenuOptionSelection(opt);
        } else if(mode === "confirm_select") {
            b.onclick = () => handleFinalConfirmation(opt);
        }
        optGrp.appendChild(b);
    });
    win.appendChild(optGrp);
    win.scrollTop = win.scrollHeight;
}

async function handleLanguageSelection(lang) {
    pushBotTextBubble(lang, "user");
    const data = await postBotData("select_lang");
    pushBotTextBubble(data.welcome, "bot");
    renderOptionButtons(data.options, "menu_select");
}



// --- Fully Optimized Script Routing Elements Layer ---

window.sendDirectBotText = async function() {
    const inp = document.getElementById("botQueryBox");
    const txt = inp.value.trim();
    if(!txt) return;
    
    pushBotTextBubble(txt, "user");
    inp.value = "";
    
    // Clear old action option stack nodes from previous turns completely to avoid confusion
    const activeStacks = document.querySelectorAll(".interactive-options-stack");
    activeStacks.forEach(stack => stack.remove());
    
    const data = await postBotData("text_query", { message: txt });
    
    // 🌟 FORCE DIRECT INJECTION - REMOVED INTERMEDIATE CONFIRMATION SELECTIONS ENTIRELY
    pushBotTextBubble(data.text, "bot");
    
    if (data.options && data.options.length > 0) {
        renderOptionButtons(data.options, "menu_select");
    }
    
    // 🌟 INJECT MEDIA STREAMS (YOUTUBE EMBEDS / LINKEDIN BLOCKS) FOR NATIVE QUERIES
    if (data.media && data.media.trim() !== "") {
        setTimeout(() => injectMediaContainer(data.media), 150);
    }
};

// Unified Option Button Stream Trigger Mapper
async function handleMenuOptionSelection(opt) {
    pushBotTextBubble(opt, "user");
    
    const activeStacks = document.querySelectorAll(".interactive-options-stack");
    activeStacks.forEach(stack => stack.remove());
    
    if (opt.includes("FAQs") || opt.includes("View College FAQs Portal")) {
        pushBotTextBubble("🔗 Opening our comprehensive Campus FAQs Portal Center now...", "bot");
        setTimeout(() => {
            window.location.href = "/faqs"; // Redirects right into the new page route!
        }, 800);
        return;
    }
    
    const data = await postBotData("select_option", { option: opt });
    pushBotTextBubble(data.text, "bot");
    
    if (data.media && data.media.trim() !== "") {
        injectMediaContainer(data.media);
    }
    if (data.options && data.options.length > 0) {
        renderOptionButtons(data.options, "menu_select");
    }
}

async function handleFinalConfirmation(choice) {
    pushBotTextBubble(choice, "user");
    if (choice.includes("Yes")) {
        pushBotTextBubble("Excellent choice! Here are the details:\n\n" + lastCachedAnswer, "bot");
    } else {
        pushBotTextBubble("No problem! Redirecting to help desk. For urgent support lines call: **08852-252233**.", "bot");
    }
}

function injectMediaContainer(htmlContent) {
    const win = document.getElementById("chatWindow");
    const mediaContainer = document.createElement("div");
    mediaContainer.innerHTML = htmlContent;
    win.appendChild(mediaContainer);
    win.scrollTop = win.scrollHeight;
}

