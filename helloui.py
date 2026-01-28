import streamlit as st
import numpy as np
import time

# ---------- Custom CSS for Advanced UI ----------
st.markdown("""
<style>
    @import url('https://fonts.googleapis.com/css2?family=Poppins:wght@300;400;600;700&display=swap');
    
    * {
        font-family: 'Poppins', sans-serif;
    }
    
    .stApp {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
    }
    
    .main-title {
        text-align: center;
        font-size: 4rem;
        font-weight: 700;
        color: white;
        text-shadow: 0 0 20px rgba(255,255,255,0.5);
        margin-bottom: 1rem;
        animation: glow 2s ease-in-out infinite alternate;
    }
    
    @keyframes glow {
        from { text-shadow: 0 0 10px #fff, 0 0 20px #fff, 0 0 30px #667eea; }
        to { text-shadow: 0 0 20px #fff, 0 0 30px #764ba2, 0 0 40px #764ba2; }
    }
    
    .game-container {
        background: rgba(255, 255, 255, 0.95);
        border-radius: 30px;
        padding: 2rem;
        box-shadow: 0 20px 60px rgba(0,0,0,0.3);
        backdrop-filter: blur(10px);
    }
    
    .score-card {
        background: linear-gradient(135deg, #f093fb 0%, #f5576c 100%);
        border-radius: 20px;
        padding: 1.5rem;
        text-align: center;
        color: white;
        box-shadow: 0 10px 30px rgba(0,0,0,0.2);
        transition: transform 0.3s;
    }
    
    .score-card:hover {
        transform: translateY(-5px);
    }
    
    .score-number {
        font-size: 3rem;
        font-weight: 700;
        margin: 0.5rem 0;
    }
    
    .score-label {
        font-size: 1.2rem;
        font-weight: 600;
        opacity: 0.9;
    }
    
    .turn-indicator {
        background: linear-gradient(135deg, #4facfe 0%, #00f2fe 100%);
        border-radius: 15px;
        padding: 1rem 2rem;
        text-align: center;
        color: white;
        font-size: 1.8rem;
        font-weight: 600;
        margin: 1.5rem 0;
        box-shadow: 0 8px 25px rgba(0,0,0,0.2);
        animation: pulse 2s infinite;
    }
    
    @keyframes pulse {
        0%, 100% { transform: scale(1); }
        50% { transform: scale(1.05); }
    }
    
    .winner-banner {
        background: linear-gradient(135deg, #ffd89b 0%, #19547b 100%);
        border-radius: 20px;
        padding: 2rem;
        text-align: center;
        color: white;
        font-size: 2.5rem;
        font-weight: 700;
        margin: 1rem 0;
        box-shadow: 0 15px 40px rgba(0,0,0,0.3);
        animation: bounceIn 0.8s;
    }
    
    @keyframes bounceIn {
        0% { transform: scale(0); }
        50% { transform: scale(1.1); }
        100% { transform: scale(1); }
    }
    
    div[data-testid="stButton"] button {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        color: white;
        border: none;
        border-radius: 15px;
        padding: 1rem 2rem;
        font-size: 1.2rem;
        font-weight: 600;
        transition: all 0.3s;
        box-shadow: 0 8px 20px rgba(0,0,0,0.2);
        width: 100%;
    }
    
    div[data-testid="stButton"] button:hover {
        transform: translateY(-3px);
        box-shadow: 0 12px 30px rgba(0,0,0,0.3);
    }
    
    .cell-button {
        min-height: 120px !important;
        font-size: 4rem !important;
        background: white !important;
        border: 3px solid #e0e0e0 !important;
        transition: all 0.3s !important;
    }
    
    .cell-button:hover {
        background: #f5f5f5 !important;
        border-color: #667eea !important;
        transform: scale(1.05) !important;
    }
    
    .winning-cell {
        background: linear-gradient(135deg, #84fab0 0%, #8fd3f4 100%) !important;
        animation: winPulse 1s infinite !important;
    }
    
    @keyframes winPulse {
        0%, 100% { transform: scale(1); }
        50% { transform: scale(1.1); }
    }
    
    .mode-selector {
        background: white;
        border-radius: 20px;
        padding: 1.5rem;
        margin: 1rem 0;
        box-shadow: 0 10px 30px rgba(0,0,0,0.1);
    }
    
    .ai-thinking {
        background: linear-gradient(135deg, #fa709a 0%, #fee140 100%);
        border-radius: 15px;
        padding: 1rem;
        text-align: center;
        color: white;
        font-weight: 600;
        animation: thinking 1.5s infinite;
    }
    
    @keyframes thinking {
        0%, 100% { opacity: 1; }
        50% { opacity: 0.5; }
    }
    
    .stSelectbox {
        border-radius: 10px;
    }
</style>
""", unsafe_allow_html=True)

# ---------- Game Logic ----------
def check_winner(b):
    """Check for winner and return winning positions"""
    # Check rows
    for i in range(3):
        if abs(np.sum(b[i, :])) == 3:
            winner = "X" if np.sum(b[i, :]) == 3 else "O"
            return winner, [(i, 0), (i, 1), (i, 2)]
    
    # Check columns
    for j in range(3):
        if abs(np.sum(b[:, j])) == 3:
            winner = "X" if np.sum(b[:, j]) == 3 else "O"
            return winner, [(0, j), (1, j), (2, j)]
    
    # Check diagonals
    if abs(np.trace(b)) == 3:
        winner = "X" if np.trace(b) == 3 else "O"
        return winner, [(0, 0), (1, 1), (2, 2)]
    
    if abs(np.trace(np.fliplr(b))) == 3:
        winner = "X" if np.trace(np.fliplr(b)) == 3 else "O"
        return winner, [(0, 2), (1, 1), (2, 0)]
    
    # Check draw
    if not 0 in b:
        return "Draw", []
    
    return None, []

def minimax(board, depth, is_maximizing, alpha=-np.inf, beta=np.inf):
    """Minimax algorithm with alpha-beta pruning"""
    result, _ = check_winner(board)
    
    if result == "O":
        return 10 - depth
    elif result == "X":
        return depth - 10
    elif result == "Draw":
        return 0
    
    if is_maximizing:
        max_score = -np.inf
        for i in range(3):
            for j in range(3):
                if board[i, j] == 0:
                    board[i, j] = -1
                    score = minimax(board, depth + 1, False, alpha, beta)
                    board[i, j] = 0
                    max_score = max(score, max_score)
                    alpha = max(alpha, score)
                    if beta <= alpha:
                        break
        return max_score
    else:
        min_score = np.inf
        for i in range(3):
            for j in range(3):
                if board[i, j] == 0:
                    board[i, j] = 1
                    score = minimax(board, depth + 1, True, alpha, beta)
                    board[i, j] = 0
                    min_score = min(score, min_score)
                    beta = min(beta, score)
                    if beta <= alpha:
                        break
        return min_score

def get_best_move(board, difficulty):
    """Get AI move based on difficulty"""
    empty_cells = [(i, j) for i in range(3) for j in range(3) if board[i, j] == 0]
    
    if difficulty == "Easy":
        return empty_cells[np.random.randint(len(empty_cells))]
    
    elif difficulty == "Medium":
        if np.random.random() < 0.5:
            return empty_cells[np.random.randint(len(empty_cells))]
    
    # Hard mode or Medium 50% of the time
    best_score = -np.inf
    best_move = None
    
    for i, j in empty_cells:
        board[i, j] = -1
        score = minimax(board.copy(), 0, False)
        board[i, j] = 0
        
        if score > best_score:
            best_score = score
            best_move = (i, j)
    
    return best_move

# ---------- Initialize Session State ----------
if "board" not in st.session_state:
    st.session_state.board = np.zeros((3, 3), dtype=int)
    st.session_state.current = 1
    st.session_state.game_over = False
    st.session_state.winner = None
    st.session_state.winning_positions = []
    st.session_state.scores = {"X": 0, "O": 0, "Draw": 0}
    st.session_state.game_mode = "Player vs Player"
    st.session_state.ai_difficulty = "Hard"
    st.session_state.total_games = 0

symbols = {0: " ", 1: "❌", -1: "⭕"}

# ---------- Header ----------
st.markdown('<h1 class="main-title">🎮 TIC TAC TOE ARENA</h1>', unsafe_allow_html=True)

# ---------- Game Mode Selection ----------
col1, col2 = st.columns(2)
with col1:
    game_mode = st.selectbox(
        "🎯 Select Game Mode",
        ["Player vs Player", "Player vs AI"],
        key="mode_select"
    )
    st.session_state.game_mode = game_mode

with col2:
    if game_mode == "Player vs AI":
        difficulty = st.selectbox(
            "🤖 AI Difficulty",
            ["Easy", "Medium", "Hard"],
            key="difficulty_select"
        )
        st.session_state.ai_difficulty = difficulty

# ---------- Score Board ----------
st.markdown("### 📊 Scoreboard")
score_cols = st.columns(3)

with score_cols[0]:
    st.markdown(f"""
    <div class="score-card">
        <div class="score-label">Player X ❌</div>
        <div class="score-number">{st.session_state.scores['X']}</div>
    </div>
    """, unsafe_allow_html=True)

with score_cols[1]:
    st.markdown(f"""
    <div class="score-card" style="background: linear-gradient(135deg, #ffd89b 0%, #19547b 100%);">
        <div class="score-label">Draws 🤝</div>
        <div class="score-number">{st.session_state.scores['Draw']}</div>
    </div>
    """, unsafe_allow_html=True)

with score_cols[2]:
    label = "AI ⭕" if game_mode == "Player vs AI" else "Player O ⭕"
    st.markdown(f"""
    <div class="score-card" style="background: linear-gradient(135deg, #4facfe 0%, #00f2fe 100%);">
        <div class="score-label">{label}</div>
        <div class="score-number">{st.session_state.scores['O']}</div>
    </div>
    """, unsafe_allow_html=True)

st.markdown("---")

# ---------- Turn Indicator ----------
if not st.session_state.game_over:
    turn = "Player X ❌" if st.session_state.current == 1 else ("AI ⭕" if game_mode == "Player vs AI" else "Player O ⭕")
    st.markdown(f'<div class="turn-indicator">Current Turn: {turn}</div>', unsafe_allow_html=True)
    
    # AI Move
    if game_mode == "Player vs AI" and st.session_state.current == -1 and not st.session_state.game_over:
        st.markdown('<div class="ai-thinking">🤖 AI is thinking...</div>', unsafe_allow_html=True)
        time.sleep(0.5)
        
        move = get_best_move(st.session_state.board.copy(), st.session_state.ai_difficulty)
        if move:
            st.session_state.board[move[0], move[1]] = -1
            
            winner, positions = check_winner(st.session_state.board)
            if winner:
                st.session_state.game_over = True
                st.session_state.winner = winner
                st.session_state.winning_positions = positions
                st.session_state.scores[winner] += 1
                st.session_state.total_games += 1
            else:
                st.session_state.current = 1
            st.rerun()

# ---------- Winner Banner ----------
if st.session_state.game_over and st.session_state.winner:
    if st.session_state.winner == "Draw":
        st.markdown('<div class="winner-banner">🤝 It\'s a Draw!</div>', unsafe_allow_html=True)
    else:
        winner_name = "AI" if (st.session_state.winner == "O" and game_mode == "Player vs AI") else f"Player {st.session_state.winner}"
        st.markdown(f'<div class="winner-banner">🏆 {winner_name} Wins! 🎉</div>', unsafe_allow_html=True)
    st.balloons()

# ---------- Game Board ----------
st.markdown("### 🎯 Game Board")
for i in range(3):
    cols = st.columns(3)
    for j in range(3):
        is_winning = (i, j) in st.session_state.winning_positions
        cell_class = "winning-cell" if is_winning else "cell-button"
        
        if cols[j].button(
            symbols[st.session_state.board[i, j]],
            key=f"{i}-{j}",
            use_container_width=True,
            disabled=st.session_state.game_over or st.session_state.board[i, j] != 0
        ):
            if st.session_state.board[i, j] == 0 and not st.session_state.game_over:
                st.session_state.board[i, j] = st.session_state.current
                
                winner, positions = check_winner(st.session_state.board)
                if winner:
                    st.session_state.game_over = True
                    st.session_state.winner = winner
                    st.session_state.winning_positions = positions
                    st.session_state.scores[winner] += 1
                    st.session_state.total_games += 1
                else:
                    st.session_state.current *= -1
                
                st.rerun()

# ---------- Control Buttons ----------
st.markdown("---")
btn_cols = st.columns(3)

with btn_cols[0]:
    if st.button("🔄 New Game", use_container_width=True):
        st.session_state.board = np.zeros((3, 3), dtype=int)
        st.session_state.current = 1
        st.session_state.game_over = False
        st.session_state.winner = None
        st.session_state.winning_positions = []
        st.rerun()

with btn_cols[1]:
    if st.button("🗑️ Reset Scores", use_container_width=True):
        st.session_state.scores = {"X": 0, "O": 0, "Draw": 0}
        st.session_state.total_games = 0
        st.rerun()

with btn_cols[2]:
    if st.button("🎲 Random First", use_container_width=True):
        st.session_state.board = np.zeros((3, 3), dtype=int)
        st.session_state.current = np.random.choice([1, -1])
        st.session_state.game_over = False
        st.session_state.winner = None
        st.session_state.winning_positions = []
        st.rerun()

# ---------- Stats ----------
if st.session_state.total_games > 0:
    st.markdown("---")
    st.markdown("### 📈 Game Statistics")
    
    stat_cols = st.columns(4)
    with stat_cols[0]:
        st.metric("Total Games", st.session_state.total_games)
    with stat_cols[1]:
        win_rate = (st.session_state.scores['X'] / st.session_state.total_games) * 100
        st.metric("X Win Rate", f"{win_rate:.1f}%")
    with stat_cols[2]:
        win_rate_o = (st.session_state.scores['O'] / st.session_state.total_games) * 100
        st.metric("O Win Rate", f"{win_rate_o:.1f}%")
    with stat_cols[3]:
        draw_rate = (st.session_state.scores['Draw'] / st.session_state.total_games) * 100
        st.metric("Draw Rate", f"{draw_rate:.1f}%")

# ---------- Footer ----------
st.markdown("---")
st.markdown(
    """
    <div style='text-align: center; color: white; padding: 1rem;'>
        <p style='font-size: 1.2rem; font-weight: 600;'>
            🎮 Advanced Tic-Tac-Toe with AI 🤖
        </p>
        <p style='opacity: 0.8;'>
            Powered by NumPy & Streamlit | AI uses Minimax Algorithm with Alpha-Beta Pruning
        </p>
    </div>
    """,
    unsafe_allow_html=True
)
