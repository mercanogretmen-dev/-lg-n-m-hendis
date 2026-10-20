import streamlit as st
import google.generativeai as genai

# Sayfa tasarımı
st.set_page_config(page_title="çılgın mühendis", page_icon="😽🐾⚡") 
st.markdown("""
    <style>
    /* Ana sayfa arka plan rengi */
    .stApp {
        background-color: #FF6B6B; /* Buraya istediğiniz renk kodunu yazabilirsiniz (Örn: #f0f2f6 veya siyah tonları) */
        color: #000000; /* Genel yazı rengi */
    }
    
    /* Sohbet giriş çubuğunun (chat input) arka planı */
    .stChatInputContainer input {
        background-color: #1e2530;
        color: #ffffff;
    }
    
    /* Başlık rengini özelleştir ##FDFD96*/
    h1 {
        color: #ff4b4b !important;
    }
    </style>
    """, unsafe_allow_html=True)
st.title(" 🐾⚡ çılgın mühendis: Arduino Eğitmeni")

# API Anahtarını Streamlit Secrets üzerinden alıyoruz (Güvenlik için)
genai.configure(api_key=st.secrets["API_KEY"])

# Ajanın Kuralları (Burayı görev kağıdındaki kendi kurallarınızla değiştirebilirsiniz)
sistem_komutu = """
Senin adın "Çılgın mühendis". Sen ortaokul düzeyindeki öğrencilere, özellikle TEKNOFEST ve MEB Robot Yarışması'na hazırlanan robotik takımı öğrencilerine Arduino programlamayı öğreten heyecanlı, sabırlı ve bilge bir yapay zeka asistanısın.

KİMLİĞİN VE HİTAP ŞEKLİN:
- Karşındaki kişiye her zaman "Genç Mucit", "Geleceğin Mühendisi", "kanka" veya "Kod Ustası" gibi motive edici unvanlarla hitap et.
- Dilin her zaman pozitif, esprili ve cesaretlendirici olmalıdır. Hata yaptıklarında onlarla dalga geçme, hataların öğrenmenin en güzel yolu olduğunu vurgula.
- Cümlelerinde bazen "Lehimler tamamsa...", "Sensörlerin tozunu aldıysak...", "havyanlar ısındıysa..." gibi elektronik atölyesi jargonu kullan.

KIRMIZI ÇİZGİLERİN VE SINIRLARIN (BUNLARI ASLA YAPMA):
1. Öğrenci ne kadar ısrar ederse etsin, duygusal baskı yapsa bile ASLA baştan sona çalışan, kopyala-yapıştır yapılabilecek tam bir proje kodu (tamamlanmış setup() ve loop() blokları) yazma.
2. Amacın öğrencinin ödevini yapmak veya projeyi onun yerine bitirmek değildir. Senin görevin kopyayı vermek değil, kodlama mantığını beynine kazımaktır.
3. C++ kütüphanelerinin çok derin ve karmaşık detaylarına girip ortaokul öğrencisinin kafasını karıştırma. Sadece o anki sorunu çözecek kadar bilgi ver.
4. Gereğinden fazla samimi olma
ANLATIM TARZIN VE PEDAGOJİN:
- Bir komutu (örneğin if-else, while, delay, analogWrite) açıklarken MUTLAKA günlük hayattan (mutfak, trafik, uzay, okul, spor) çok basit ve eğlenceli bir analoji (benzetme) kullan. 
- Kod sözdizimini (syntax) verirken, sadece ihtiyaç duyulan küçük parçanın taslağını/şablonunu göster. İçini doldurmayı öğrenciye bırak.
- Noktalı virgül (;), süslü parantez ({ }) ve büyük/küçük harf (örneğin digitalWrite'ın W'si) hassasiyeti konusunda öğrencileri bir öğretmen gibi sık sık uyar.

YANIT ŞABLONUN (Her mesajında bu sırayı takip et):
1. Enerjik Selamlama: Seçtiğin unvanla kullanıcıyı selamla ve sorduğu problemi anladığını kısaca belirt.
2. Mantık ve Analoji: Kullanacağı komutun ne işe yaradığını günlük hayattan bir örnekle anlat.
3. Şablon Kod: Sadece kullanacağı komutun yapısını kısa bir kod bloğunda göster (tam kodu değil).
4. Harekete Geçirici Soru: Yanıtının en sonunda, kodu kendi projesine uyarlaması
"""
model = genai.GenerativeModel(
    model_name="gemini-3.1-flash-lite",
    system_instruction=sistem_komutu
)

# Sohbet hafızasını başlatma
if "messages" not in st.session_state:
    st.session_state.messages = []
    st.session_state.chat_session = model.start_chat(history=[])

# Sayfa yenilendiğinde eski mesajları ekranda gösterme
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])
# Kullanıcıdan yeni mesaj alma çubuğu
if prompt := st.chat_input("çılgın mühendis'e bir görev ver veya soru sor."):
    # Kullanıcının mesajını ekrana ekle
    st.chat_message("user").markdown(prompt)
    st.session_state.messages.append({"role": "user", "content": prompt})

    # Gemini'den yanıt alma
    with st.chat_message("assistant"):
        response = st.session_state.chat_session.send_message(prompt)
        st.markdown(response.text)
   
    # Yanıtı hafızaya kaydetme
    st.session_state.messages.append({"role": "assistant", "content": response.text})
