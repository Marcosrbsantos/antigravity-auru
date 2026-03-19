function initDashboard() {
    // Animação das barras do gráfico
    const bars = document.querySelectorAll('.chart-bar');
    bars.forEach((bar, index) => {
        const targetHeight = bar.style.height || '70%';
        bar.style.height = '0%';
        setTimeout(() => {
            bar.style.height = targetHeight;
        }, 200 + (index * 100));
    });

    updateScale(75, 25); // 75% gastos / 25% disponível
}

function updateScale(expensePercent, incomePercent) {
    const expenseFill = document.getElementById('scale-expense');
    if (expenseFill) {
        expenseFill.style.width = `${expensePercent}%`;
        expenseFill.style.left = '0%';
    }
}

// Navegação entre Abas
const navItems = document.querySelectorAll('.nav-item');
const views = document.querySelectorAll('.view-section');

navItems.forEach((item, index) => {
    item.addEventListener('click', (e) => {
        e.preventDefault();
        
        navItems.forEach(nav => nav.classList.remove('active'));
        item.classList.add('active');

        const viewMap = ['home', 'analytics', 'cards', 'profile'];
        // O scanner btn é o terceiro item (index 2), então compensamos
        let viewKey = index;
        if (index === 2) return; // Ignorar clique no scanner para navegação de abas
        if (index > 2) viewKey = index - 1;
        
        const targetViewId = `view-${viewMap[viewKey]}`;
        
        views.forEach(view => {
            view.classList.remove('active');
            if(view.id === targetViewId) {
                view.classList.add('active');
            }
        });

        if (targetViewId === 'view-home') {
            initDashboard();
        }
    });
});

document.addEventListener('DOMContentLoaded', initDashboard);

document.getElementById('scanner-btn').addEventListener('click', () => {
    alert('Auru iniciou o escaneamento do recibo...');
});
