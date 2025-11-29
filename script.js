/*
 * NAPTHE WEB - JavaScript
 * Xu ly logic cho trang nap the
 * 
 * Luong hoat dong:
 * 1. Khi trang load -> kiem tra user ID trong URL hoac localStorage
 * 2. Neu co user ID -> hien form nap the
 * 3. Neu khong co -> hien form nhap username de tim user
 * 4. Khi nap the -> goi API /api/charge
 * 5. Luu lich su vao localStorage
 */

// ============================================
// CAU HINH
// ============================================
// API_BASE: de trong vi API cung domain
const API_BASE = '';

// ============================================
// BIEN TOAN CUC
// ============================================
let currentUserId = null; // Luu user ID hien tai
let currentUsername = null; // Luu username hien tai
let currentAvatar = null; // Luu avatar URL hien tai

// ============================================
// KHOI TAO KHI TRANG LOAD
// ============================================
document.addEventListener('DOMContentLoaded', () => {
    initApp();
});

/*
 * Khoi tao ung dung
 * - Kiem tra user ID tu URL param (?uid=xxx)
 * - Neu co thi luu vao localStorage
 * - Neu khong thi lay tu localStorage
 * - Hien thi giao dien phu hop
 */
async function initApp() {
    // Lay user ID tu URL (khi user click link tu Discord)
    const urlParams = new URLSearchParams(window.location.search);
    const userIdFromUrl = urlParams.get('uid');
    const usernameFromUrl = urlParams.get('username');
    const avatarFromUrl = urlParams.get('avatar');
    
    if (userIdFromUrl) {
        // Luu vao localStorage de giu lai khi reload
        localStorage.setItem('discord_user_id', userIdFromUrl);
        currentUserId = userIdFromUrl;
        
        // Neu co username va avatar tu URL thi luu luon
        if (usernameFromUrl) {
            localStorage.setItem('discord_username', usernameFromUrl);
            currentUsername = usernameFromUrl;
        }
        if (avatarFromUrl) {
            localStorage.setItem('discord_avatar', decodeURIComponent(avatarFromUrl));
            currentAvatar = decodeURIComponent(avatarFromUrl);
        }
        
        // Neu chua co username/avatar, thu fetch tu API
        if (!currentUsername || !currentAvatar) {
            await fetchUserInfo(userIdFromUrl);
        }
        
        // Xoa param khoi URL cho sach
        window.history.replaceState({}, document.title, window.location.pathname);
    } else {
        // Lay tu localStorage
        currentUserId = localStorage.getItem('discord_user_id');
        currentUsername = localStorage.getItem('discord_username') || null;
        currentAvatar = localStorage.getItem('discord_avatar') || null;
    }

    // Hien thi giao dien phu hop
    if (currentUserId) {
        showUserInfo(currentUserId, currentUsername, currentAvatar);
        showNaptheForm();
    } else {
        showUserForm();
    }

    // Load lich su nap the tu localStorage
    loadHistory();

    // Gan event listeners
    document.getElementById('search-user').addEventListener('click', searchUser);
    document.getElementById('username-input').addEventListener('keypress', (e) => {
        if (e.key === 'Enter') searchUser();
    });
    document.getElementById('change-user').addEventListener('click', changeUser);
    document.getElementById('submit-btn').addEventListener('click', submitCard);
}

// ============================================
// QUAN LY USER
// ============================================

/*
 * Hien thi thong tin user da chon
 */
function showUserInfo(userId, username, avatar) {
    document.getElementById('user-info').classList.remove('hidden');
    document.getElementById('user-form').classList.add('hidden');
    document.getElementById('display-user-id').textContent = userId;
    document.getElementById('display-username').textContent = username || 'Unknown';
    document.getElementById('display-avatar').src = avatar || 'https://cdn.discordapp.com/embed/avatars/0.png';
}

/*
 * Fetch thong tin user tu API bang user ID
 */
async function fetchUserInfo(userId) {
    try {
        const response = await fetch(`${API_BASE}/api/get-user?uid=${encodeURIComponent(userId)}`);
        const data = await response.json();
        
        if (data.success && data.user) {
            currentUsername = data.user.username || null;
            currentAvatar = data.user.avatar || null;
            if (currentUsername) {
                localStorage.setItem('discord_username', currentUsername);
            } else {
                localStorage.removeItem('discord_username');
            }
            if (currentAvatar) {
                localStorage.setItem('discord_avatar', currentAvatar);
            } else {
                localStorage.removeItem('discord_avatar');
            }
        }
    } catch (error) {
        console.error('Loi khi lay thong tin user:', error);
    }
}

/*
 * Hien thi form nhap username
 */
function showUserForm() {
    document.getElementById('user-info').classList.add('hidden');
    document.getElementById('user-form').classList.remove('hidden');
    document.getElementById('napthe-form').classList.add('hidden');
}

/*
 * Hien thi form nap the
 */
function showNaptheForm() {
    document.getElementById('napthe-form').classList.remove('hidden');
}

/*
 * Doi user khac
 */
function changeUser() {
    localStorage.removeItem('discord_user_id');
    localStorage.removeItem('discord_username');
    localStorage.removeItem('discord_avatar');
    currentUserId = null;
    currentUsername = null;
    currentAvatar = null;
    showUserForm();
}

/*
 * Tim user theo username
 * Goi API /api/search-user de tim trong server Discord
 */
async function searchUser() {
    const username = document.getElementById('username-input').value.trim();
    if (!username) {
        showSearchError('Vui long nhap username');
        return;
    }

    const searchBtn = document.getElementById('search-user');
    searchBtn.disabled = true;
    searchBtn.textContent = 'Dang tim...';
    hideSearchError();

    try {
        // Goi API tim user
        const response = await fetch(`${API_BASE}/api/search-user?username=${encodeURIComponent(username)}`);
        const data = await response.json();

        if (data.success && data.users && data.users.length > 0) {
            // Hien thi danh sach ket qua
            showSearchResults(data.users);
        } else {
            showSearchError(data.message || 'Khong tim thay user nao');
        }
    } catch (error) {
        showSearchError('Loi ket noi. Vui long thu lai.');
        console.error(error);
    } finally {
        searchBtn.disabled = false;
        searchBtn.textContent = 'Tim';
    }
}

/*
 * Hien thi danh sach ket qua tim kiem
 */
function showSearchResults(users) {
    const container = document.getElementById('search-results');
    container.innerHTML = '';
    container.classList.remove('hidden');

    users.forEach(user => {
        const item = document.createElement('div');
        item.className = 'search-result-item';
        item.innerHTML = `
            <img src="${user.avatar || 'https://cdn.discordapp.com/embed/avatars/0.png'}" alt="avatar">
            <span class="name">${user.username}</span>
            <span class="id">${user.id}</span>
        `;
        // Click de chon user nay - truyen them username va avatar
        item.addEventListener('click', () => selectUser(user.id, user.username, user.avatar));
        container.appendChild(item);
    });
}

/*
 * Chon user tu ket qua tim kiem
 */
function selectUser(userId, username, avatar) {
    localStorage.setItem('discord_user_id', userId);
    if (username) {
        localStorage.setItem('discord_username', username);
    } else {
        localStorage.removeItem('discord_username');
    }
    if (avatar) {
        localStorage.setItem('discord_avatar', avatar);
    } else {
        localStorage.removeItem('discord_avatar');
    }
    currentUserId = userId;
    currentUsername = username || null;
    currentAvatar = avatar || null;
    showUserInfo(userId, username, avatar);
    showNaptheForm();
    document.getElementById('search-results').classList.add('hidden');
}

/*
 * Hien thi loi tim kiem
 */
function showSearchError(message) {
    const errorEl = document.getElementById('search-error');
    errorEl.textContent = message;
    errorEl.classList.remove('hidden');
}

/*
 * An thong bao loi
 */
function hideSearchError() {
    document.getElementById('search-error').classList.add('hidden');
    document.getElementById('search-results').classList.add('hidden');
}

// ============================================
// NAP THE
// ============================================

/*
 * Gui the nap
 * Goi API /api/charge de gui the len thesieure.com
 */
async function submitCard() {
    // Kiem tra da chon user chua
    if (!currentUserId) {
        showResult('Vui long chon user truoc', 'error');
        return;
    }

    // Lay thong tin tu form
    const nhamang = document.getElementById('nhamang').value;
    const menhgia = document.getElementById('menhgia').value;
    const seri = document.getElementById('seri').value.trim();
    const mathe = document.getElementById('mathe').value.trim();
    const voucher = document.getElementById('voucher').value.trim();

    // Validate
    if (!seri || !mathe) {
        showResult('Vui long nhap day du so seri va ma the', 'error');
        return;
    }

    // Hien thi loading
    const submitBtn = document.getElementById('submit-btn');
    submitBtn.disabled = true;
    showLoading(true);
    hideResult();

    try {
        // Goi API nap the
        const response = await fetch(`${API_BASE}/api/charge`, {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json'
            },
            body: JSON.stringify({
                user_id: currentUserId,
                telco: nhamang,
                amount: parseInt(menhgia),
                serial: seri,
                code: mathe,
                voucher: voucher || null
            })
        });

        const data = await response.json();

        if (data.success) {
            if (data.status === 99) {
                // The dang xu ly
                showResult(`The dang duoc xu ly. Ma giao dich: ${data.request_id}`, 'pending');
            } else if (data.status === 1) {
                // The thanh cong
                showResult(`Nap the thanh cong! Nhan duoc: ${formatMoney(data.amount)} VND`, 'success');
            }
            // Luu vao lich su
            addToHistory({
                request_id: data.request_id,
                telco: nhamang,
                amount: menhgia,
                status: data.status,
                time: new Date().toLocaleString('vi-VN')
            });
            // Xoa form
            clearForm();
        } else {
            showResult(data.message || 'Co loi xay ra', 'error');
        }
    } catch (error) {
        showResult('Loi ket noi. Vui long thu lai.', 'error');
        console.error(error);
    } finally {
        submitBtn.disabled = false;
        showLoading(false);
    }
}

// ============================================
// UI HELPERS
// ============================================

/*
 * Hien/an loading spinner
 */
function showLoading(show) {
    const loading = document.getElementById('loading');
    const form = document.getElementById('napthe-form');
    
    if (show) {
        loading.classList.remove('hidden');
        form.classList.add('hidden');
    } else {
        loading.classList.add('hidden');
        form.classList.remove('hidden');
    }
}

/*
 * Hien thi ket qua nap the
 * @param message - Noi dung thong bao
 * @param type - 'success', 'error', hoac 'pending'
 */
function showResult(message, type) {
    const result = document.getElementById('result');
    result.textContent = message;
    result.className = `result ${type}`;
    result.classList.remove('hidden');
}

/*
 * An thong bao ket qua
 */
function hideResult() {
    document.getElementById('result').classList.add('hidden');
}

/*
 * Xoa form sau khi nap thanh cong
 */
function clearForm() {
    document.getElementById('seri').value = '';
    document.getElementById('mathe').value = '';
    document.getElementById('voucher').value = '';
}

/*
 * Format so tien thanh dang 1,000,000
 */
function formatMoney(amount) {
    return new Intl.NumberFormat('vi-VN').format(amount);
}

// ============================================
// LICH SU NAP THE
// ============================================

/*
 * Load lich su tu localStorage
 */
function loadHistory() {
    const history = JSON.parse(localStorage.getItem('napthe_history') || '[]');
    renderHistory(history);
}

/*
 * Them giao dich vao lich su
 */
function addToHistory(item) {
    const history = JSON.parse(localStorage.getItem('napthe_history') || '[]');
    history.unshift(item); // Them vao dau
    if (history.length > 20) history.pop(); // Giu toi da 20 giao dich
    localStorage.setItem('napthe_history', JSON.stringify(history));
    renderHistory(history);
}

/*
 * Render danh sach lich su ra giao dien
 */
function renderHistory(history) {
    const container = document.getElementById('history-list');
    
    if (history.length === 0) {
        container.innerHTML = '<p class="empty">Chua co giao dich nao</p>';
        return;
    }

    container.innerHTML = history.map(item => {
        // Xac dinh trang thai
        let statusText, statusClass;
        if (item.status === 99) {
            statusText = 'Dang xu ly';
            statusClass = 'pending';
        } else if (item.status === 1) {
            statusText = 'Thanh cong';
            statusClass = 'success';
        } else {
            statusText = 'That bai';
            statusClass = 'error';
        }

        return `
            <div class="history-item">
                <div>${item.telco} - ${formatMoney(item.amount)} VND</div>
                <div style="font-size: 0.8rem; color: rgba(255,255,255,0.5); margin-top: 5px;">
                    ${item.time}
                    <span class="status ${statusClass}">${statusText}</span>
                </div>
            </div>
        `;
    }).join('');
}
