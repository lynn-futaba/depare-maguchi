// --- 共通トースト通知機能 (Stacking Toast System) ---

function showInfo(message, duration = 5000) {
    createToast(message, 'info', duration);
}

function showError(message, duration = 7000) {
    createToast(message, 'error', duration);
}

function createToast(message, type, duration) {
    // 1. Containerの取得または作成 (Get or Create Container)
    let container = document.getElementById("toast-container");
    if (!container) {
        container = document.createElement("div");
        container.id = "toast-container";
        container.style.cssText = `
            position: fixed;
            top: 60px;          /* Initial top spacing */
            right: 30px;
            z-index: 10000;
            display: flex;
            flex-direction: column;
            gap: 15px;          /* スペースを空ける (Spacing between toasts) */
            pointer-events: none;
        `;
        document.body.appendChild(container);
    }

    // 2. デザイン設定 (Design Settings)
    const isError = type === 'error';
    const bgColor = isError ? '#c62828' : '#2e7d32'; 
    const accentColor = isError ? '#ff8a80' : '#a5d6a7';
    const label = isError ? '【システム異常】' : '【システム通知】';

    // 3. 個別のトースト作成 (Create Individual Toast)
    const toast = document.createElement("div");
    toast.style.cssText = `
        width: 550px;
        background: ${bgColor};
        color: #ffffff;
        padding: 20px 30px;
        border-radius: 4px;
        border-left: 20px solid ${accentColor};
        font-size: 26px;
        font-weight: bold;
        font-family: "Meiryo", "MS PGothic", sans-serif;
        box-shadow: 0 10px 30px rgba(0,0,0,0.5);
        text-align: left;
        pointer-events: auto; /* Clickable if you want to add a close button later */
        transition: all 0.4s ease;
        opacity: 0;
        transform: translateX(100px); /* Side slide-in animation */
        line-height: 1.4;
    `;

    toast.innerHTML = `
        <div style="font-size: 0.6em; margin-bottom: 5px; opacity: 0.9;">${label}</div>
        <div>${message}</div>
    `;

    container.appendChild(toast);

    // 4. 表示アニメーション (Show Animation)
    setTimeout(() => {
        toast.style.opacity = "1";
        toast.style.transform = "translateX(0)";
    }, 10);

    // 5. 自動削除 (Auto Remove)
    setTimeout(() => {
        toast.style.opacity = "0";
        toast.style.transform = "translateX(100px)";
        setTimeout(() => {
            if (toast.parentNode === container) {
                container.removeChild(toast);
            }
            // コンテナが空になったらコンテナ自体も消す (Optional)
            if (container.childNodes.length === 0) {
                container.remove();
            }
        }, 400);
    }, duration);
}