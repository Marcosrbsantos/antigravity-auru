let appState = {
    user: null,
    balance: parseFloat(localStorage.getItem('auru_balance') || '0'),
    expenses: 0,
    transactions: []
};

function initApp() {
    const savedUser = localStorage.getItem('auru_user');
    if (savedUser) {
        showMainApp(savedUser);
    }
    updateBalanceDisplay();
}

function selectProfile(name) {
    localStorage.setItem('auru_user', name);
    const splash = document.getElementById('splash-screen');
    splash.style.opacity = '0';
    setTimeout(() => {
        splash.style.display = 'none';
        showMainApp(name);
    }, 500);
}

function showMainApp(name) {
    appState.user = name;
    document.getElementById('main-app').style.display = 'flex';
    document.getElementById('user-display-name').textContent = name;
    document.getElementById('profile-name').textContent = name;
    
    // Customização visual por perfil
    const avatar = document.getElementById('current-user-avatar');
    const avatarLarge = document.getElementById('profile-avatar-large');
    const gradient = name === 'Marcos' 
        ? 'linear-gradient(45deg, #2196F3, #00BCD4)' 
        : 'linear-gradient(45deg, #E91E63, #9C27B0)';
    
    avatar.style.background = gradient;
    if(avatarLarge) avatarLarge.style.background = gradient;
}

function updateBalanceDisplay() {
    const balanceEl = document.getElementById('current-balance');
    const spentEl = document.getElementById('total-spending');
    const remainingEl = document.getElementById('remaining-value');
    
    const remaining = appState.balance - appState.expenses;
    
    if(balanceEl) balanceEl.textContent = `R$ ${appState.balance.toLocaleString('pt-BR', {minimumFractionDigits: 2})}`;
    if(spentEl) spentEl.textContent = `R$ ${appState.expenses.toLocaleString('pt-BR', {minimumFractionDigits: 2})}`;
    
    if(remainingEl) {
        remainingEl.textContent = `R$ ${remaining.toLocaleString('pt-BR', {minimumFractionDigits: 2})}`;
        remainingEl.style.color = remaining > 0 ? 'var(--success)' : (remaining < 0 ? 'var(--danger)' : 'white');
    }
}

function addFunds() {
    const value = prompt("Quanto deseja adicionar ao saldo?", "50,00");
    if(value) {
        const amount = parseFloat(value.replace(',', '.'));
        if(!isNaN(amount)) {
            appState.balance += amount;
            localStorage.setItem('auru_balance', appState.balance);
            updateBalanceDisplay();
        }
    }
}

function switchView(viewKey, index) {
    const navItems = document.querySelectorAll('.nav-item');
    const views = document.querySelectorAll('.view-section');
    
    navItems.forEach(nav => nav.classList.remove('active'));
    // Achar o item correto baseado no index passado
    navItems[index].classList.add('active');

    const targetId = `view-${viewKey}`;
    views.forEach(view => {
        view.classList.remove('active');
        if(view.id === targetId) view.classList.add('active');
    });

    if(viewKey === 'home') initDashboard();
}

function initDashboard() {
    // Animação das barras (seriam dados reais no futuro)
    const container = document.getElementById('spending-chart');
    if(container && container.children.length === 0) {
        for(let i=0; i<5; i++) {
            const bar = document.createElement('div');
            bar.className = 'chart-bar';
            bar.style.height = '0%';
            container.appendChild(bar);
            setTimeout(() => bar.style.height = `${Math.random()*70 + 10}%`, 200 + i*100);
        }
    }
}

function logout() {
    localStorage.clear();
    location.reload();
}

document.addEventListener('DOMContentLoaded', initApp);

document.getElementById('scanner-btn').addEventListener('click', () => {
    alert('Auru iniciou o escaneamento do recibo... (Modo Teste)');
});
