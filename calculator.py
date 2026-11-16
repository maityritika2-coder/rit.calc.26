import math
import streamlit as st

# ---------------- PAGE CONFIGURATION ----------------
st.set_page_config(
    page_title="Smart Calculator",
    page_icon="🧮",
    layout="centered"
)

# ---------------- CUSTOM CSS ----------------
st.markdown("""
<style>
    .stApp {
        background: linear-gradient(135deg, #101827, #1e293b);
        color: white;
    }

    h1 {
        text-align: center;
        color: #60A5FA;
        font-size: 42px !important;
    }

    .subtitle {
        text-align: center;
        color: #CBD5E1;
        font-size: 16px;
        margin-bottom: 30px;
    }

    .result-box {
        background: #1E293B;
        padding: 25px;
        border-radius: 15px;
        border: 1px solid #334155;
        text-align: center;
        margin-top: 20px;
    }

    .result-label {
        color: #94A3B8;
        font-size: 16px;
    }

    .result-value {
        color: #60A5FA;
        font-size: 35px;
        font-weight: bold;
        overflow-wrap: anywhere;
    }

    div.stButton > button {
        background-color: #2563EB;
        color: white;
        border-radius: 10px;
        border: none;
        min-height: 48px;
        width: 100%;
        font-weight: bold;
    }

    div.stButton > button:hover {
        background-color: #1D4ED8;
        color: white;
    }

    [data-testid="stSidebar"] {
        background-color: #172337;
    }
</style>
""", unsafe_allow_html=True)

# ---------------- SESSION STATE ----------------
if "history" not in st.session_state:
    st.session_state.history = []

# ---------------- HEADER ----------------
st.markdown("<h1>🧮 Smart Calculator</h1>", unsafe_allow_html=True)
st.markdown(
    '<p class="subtitle">A simple and powerful calculator for everyday calculations.</p>',
    unsafe_allow_html=True
)

st.divider()

# ---------------- CALCULATOR ----------------
st.subheader("Calculator")

operation = st.selectbox(
    "Select an Operation",
    [
        "Addition (+)",
        "Subtraction (-)",
        "Multiplication (×)",
        "Division (÷)"
    ]
)

numbers_input = ""

if operation in ["Addition (+)", "Multiplication (×)"]:
    numbers_input = st.text_input(
        "Enter numbers separated by commas",
        placeholder="Example: 10, 20, 30"
    )
else:
    col1, col2 = st.columns(2)

    with col1:
        num1 = st.number_input("First Number", value=0.0, format="%.6f")

    with col2:
        num2 = st.number_input("Second Number", value=0.0, format="%.6f")

# ---------------- CALCULATION ----------------
if st.button("Calculate"):
    try:
        if operation in ["Addition (+)", "Multiplication (×)"]:
            if not numbers_input.strip():
                st.warning("Please enter at least one number.")
            else:
                numbers = [float(value.strip()) for value in numbers_input.split(",")]

                if not all(math.isfinite(value) for value in numbers):
                    raise ValueError

                if operation == "Addition (+)":
                    result = sum(numbers)
                    expression = " + ".join(map(str, numbers))
                else:
                    result = math.prod(numbers)
                    expression = " × ".join(map(str, numbers))

                st.session_state.history.append(f"{expression} = {result}")

                st.markdown(
                    f"""
                    <div class="result-box">
                        <div class="result-label">Your Result</div>
                        <div class="result-value">{result:,.6f}</div>
                    </div>
                    """,
                    unsafe_allow_html=True
                )

        else:
            if not math.isfinite(num1) or not math.isfinite(num2):
                raise ValueError

            if operation == "Subtraction (-)":
                result1 = num1 - num2
                result2 = num2 - num1

                st.success(f"{num1} - {num2} = {result1}")
                st.success(f"{num2} - {num1} = {result2}")

                st.session_state.history.append(f"{num1} - {num2} = {result1}")
                st.session_state.history.append(f"{num2} - {num1} = {result2}")

            elif operation == "Division (÷)":
                if num2 == 0:
                    st.error("You cannot divide by zero!")
                else:
                    result = num1 / num2

                    st.markdown(
                        f"""
                        <div class="result-box">
                            <div class="result-label">Your Result</div>
                            <div class="result-value">{result:,.6f}</div>
                        </div>
                        """,
                        unsafe_allow_html=True
                    )

                    st.session_state.history.append(f"{num1} ÷ {num2} = {result}")

    except (ValueError, OverflowError):
        st.error("Invalid input. Please enter valid finite numbers separated by commas.")

# ---------------- CALCULATION HISTORY ----------------
st.divider()
st.subheader("📜 Calculation History")

if st.session_state.history:
    for index, item in enumerate(reversed(st.session_state.history), start=1):
        st.write(f"**{index}.** {item}")

    if st.button("Clear History"):
        st.session_state.history = []
        st.rerun()
else:
    st.info("Your calculation history will appear here.")

# ---------------- FOOTER ----------------
st.divider()
st.markdown(
    "<p style='text-align:center;color:#94A3B8;'>"
    "Smart Calculator | Built with Python & Streamlit"
    "</p>",
    unsafe_allow_html=True
)
