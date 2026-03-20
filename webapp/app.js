let appState = {
    user: null,
    balance: parseFloat(localStorage.getItem('auru_balance') || '0'),
    expenses: 0,
    transactions: [],
    subscriptions: JSON.parse(localStorage.getItem('auru_subs') || '[]')
};

function initApp() {
    const savedUser = localStorage.getItem('auru_user');
    const savedPhoto = localStorage.getItem(`auru_photo_${savedUser}`);
    
    if (savedUser) {
        showMainApp(savedUser);
        if(savedPhoto) {
            updateUserPhoto(savedPhoto);
        }
    }
    updateBalanceDisplay();
    renderSubscriptions();
}

function selectProfile(name) {
    localStorage.setItem('auru_user', name);
    // Resetar estado para o novo usuário se necessário
    location.reload(); 
}

function showMainApp(name) {
    appState.user = name;
    const splash = document.getElementById('splash-screen');
    if(splash) splash.style.display = 'none';
    
    document.getElementById('main-app').style.display = 'flex';
    document.getElementById('user-display-name').textContent = name;
    document.getElementById('profile-name').innerHTML = `${name} <span onclick="editName()" style="cursor:pointer; font-size:0.8rem; opacity:0.6;">✎</span>`;
    
    // Customização visual por perfil
    const avatar = document.getElementById('current-user-avatar');
    const avatarLarge = document.getElementById('profile-avatar-large');
    const gradient = name === 'Marcos' 
        ? 'linear-gradient(45deg, #2196F3, #00BCD4)' 
        : 'linear-gradient(45deg, #E91E63, #9C27B0)';
    
    avatar.style.background = gradient;
    if(avatarLarge) avatarLarge.style.background = gradient;
}

function editName() {
    const newName = prompt("Como deseja ser chamado?", appState.user);
    if(newName) {
        localStorage.setItem('auru_user', newName);
        location.reload();
    }
}

document.getElementById('avatar-upload')?.addEventListener('change', (e) => {
    const file = e.target.files[0];
    if(file) {
        const reader = new FileReader();
        reader.onload = (event) => {
            const photoData = event.target.result;
            localStorage.setItem(`auru_photo_${appState.user}`, photoData);
            updateUserPhoto(photoData);
        };
        reader.readAsDataURL(file);
    }
});

function updateUserPhoto(data) {
    const avatar = document.getElementById('current-user-avatar');
    const avatarLarge = document.getElementById('profile-avatar-large');
    
    if(avatar) {
        avatar.style.backgroundImage = `url(${data})`;
        avatar.style.backgroundSize = 'cover';
    }
    if(avatarLarge) {
        avatarLarge.style.backgroundImage = `url(${data})`;
        avatarLarge.style.backgroundSize = 'cover';
    }
}

function openAddSubscription() {
    const name = prompt("Nome da Assinatura (ex: Netflix):");
    const val = prompt("Valor Mensal:", "39,90");
    if(name && val) {
        const amount = parseFloat(val.replace(',', '.'));
        appState.subscriptions.push({ name, amount, icon: '💳' });
        localStorage.setItem('auru_subs', JSON.stringify(appState.subscriptions));
        renderSubscriptions();
    }
}

function renderSubscriptions() {
    const list = document.getElementById('card-transactions-list');
    if(!list) return;
    
    if(appState.subscriptions.length === 0) {
        list.innerHTML = '<div class="empty-state">Sem assinaturas registradas.</div>';
        return;
    }

    list.innerHTML = appState.subscriptions.map(s => `
        <div class="card-item">
            <div class="icon-box">${s.icon}</div>
            <div style="flex: 1">
                <p>${s.name}</p>
                <small style="color: var(--text-med)">Assinatura Mensal</small>
            </div>
            <span>R$ ${s.amount.toFixed(2)}</span>
        </div>
    `).join('');
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
    document.getElementById('real-scanner-input').click();
});

document.getElementById('real-scanner-input').addEventListener('change', async (e) => {
    const file = e.target.files[0];
    if (!file) return;

    alert('🔎 Auru está analisando sua nota... Aguarde um instante.');

    const reader = new FileReader();
    reader.onloadend = async () => {
        const base64String = reader.result.replace('data:', '').replace(/^.+,/, '');
        
        try {
            const response = await fetch('/api/process_receipt', {
                method: 'POST',
                headers: { 'Content-Type': 'application/json' },
                body: JSON.stringify({ image: base64String })
            });

            if (!response.ok) throw new Error('Erro na análise da IA');

            const data = await response.json();
            showReviewModal(data);

        } catch (error) {
            console.error(error);
            alert('❌ Erro: Não consegui ler esta nota. Tente novamente.');
        }
    };
    reader.readAsDataURL(file);
});

let currentReviewData = null;

function showReviewModal(data) {
    currentReviewData = data;
    document.getElementById('review-merchant').textContent = data.merchant;
    document.getElementById('review-modal').style.display = 'flex';
    
    renderReviewItems();
}

function renderReviewItems() {
    const list = document.getElementById('review-items-list');
    list.innerHTML = currentReviewData.items.map((item, index) => `
        <div class="review-item">
            <span style="font-size: 1.2rem">${item.icon || '📦'}</span>
            <input type="text" value="${item.name}" onchange="updateItemName(${index}, this.value)">
            <input type="text" class="price-input" value="${item.price.toFixed(2)}" onchange="updateItemPrice(${index}, this.value)">
        </div>
    `).join('');
    
    updateReviewTotal();
}

function updateItemName(index, val) { 
    currentReviewData.items[index].name = val; 
}

function updateItemPrice(index, val) { 
    currentReviewData.items[index].price = parseFloat(val.replace(',', '.'));
    updateReviewTotal();
}

function updateReviewTotal() {
    const total = currentReviewData.items.reduce((acc, i) => acc + i.price, 0);
    currentReviewData.total = total;
    document.getElementById('review-total-value').textContent = `R$ ${total.toLocaleString('pt-BR', {minimumFractionDigits: 2})}`;
}

function confirmPurchase() {
    // Adicionar à lista global
    appState.expenses += currentReviewData.total;
    appState.transactions.unshift({
        merchant: currentReviewData.merchant,
        amount: currentReviewData.total,
        date: new Date().toLocaleTimeString(),
        type: 'compra'
    });

    updateBalanceDisplay();
    renderTransactions();
    closeReview();
    alert('✅ Compra salva com sucesso!');
}

function closeReview() {
    document.getElementById('review-modal').style.display = 'none';
    currentReviewData = null;
}

function renderTransactions() {
    const list = document.getElementById('transaction-history');
    if (!list) return;
    
    if (appState.transactions.length === 0) {
        list.innerHTML = '<div class="empty-state">Scaneie uma nota para começar.</div>';
        return;
    }

    list.innerHTML = appState.transactions.map(t => `
        <div class="card-item">
            <div class="icon-box">${t.type === 'compra' ? '🛒' : '📄'}</div>
            <div style="flex: 1">
                <p>${t.merchant}</p>
                <small style="color: var(--text-med)">${t.date}</small>
            </div>
            <span class="amount expense">- R$ ${t.amount.toLocaleString('pt-BR')}</span>
        </div>
    `).join('');
}
