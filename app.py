# coding=utf8
from cgi import test
from flask import Flask, request, make_response
from flask_pymongo import PyMongo

import requests
import urllib
import urllib.request 
import os
import numpy as np
import pandas as pd
import re
import json

import threading
import time
import cv2

#lt --port 8000

import keras
from keras.preprocessing.image import ImageDataGenerator, img_to_array, load_img
from keras.models import load_model
from keras.applications.vgg19 import VGG19, preprocess_input, decode_predictions


from twilio.rest import Client

opener = urllib.request.build_opener()
opener.addheaders = [('User-agent', 'Mozilla/5.0')]
urllib.request.install_opener(opener)


app = Flask(__name__, static_url_path='/src')
model = load_model("Own Path:/best_model.h5")


account_sid = ""
auth_token = ""


eng_greet = """ Welcome to the real-time plant disease detection system! 
                This software can easily detect different diseases from a photo.
            Please take a photo with clear disease spots from leaf!"""
mal_greet = """തത്സമയ സസ്യരോഗ കണ്ടെത്തൽ സംവിധാനത്തിലേക്ക് സ്വാഗതം! 
                ഒരു ഫോട്ടോയിൽ നിന്ന് വ്യത്യസ്ത രോഗങ്ങളെ ഈ സോഫ്റ്റ്‌വെയറിന് എളുപ്പത്തിൽ കണ്ടെത്താനാകും.
                ഇലയിൽ നിന്ന് വ്യക്തമായ രോഗ പാടുകളുള്ള ഫോട്ടോ എടുക്കുക!
               👉 എത്രത്തോളം അടുത്തുനിന്ന് എടുക്കാമോ അത്രയും അടുത്ത് നിന്ന് എടുക്കുക. """
hindi_greet = """रीयल-टाइम प्लांट डिजीज डिटेक्शन सिस्टम में आपका स्वागत है! 
                    यह सॉफ्टवेयर एक फोटो से अलग-अलग बीमारियों का आसानी से पता लगा सकता है।
                    कृपया पत्ते से रोग के स्पष्ट धब्बे के साथ एक फोटो लें!
                👉 जितना पास हो सके ले लो।"""
tamil_greet = """நிகழ்நேர தாவர நோய் கண்டறிதல் அமைப்புக்கு வரவேற்கிறோம்! 
                    இந்த மென்பொருள் ஒரு புகைப்படத்தில் இருந்து பல்வேறு நோய்களை எளிதில் கண்டறிய முடியும்.
                    இலையிலிருந்து தெளிவான நோய் புள்ளிகளுடன் புகைப்படம் எடுக்கவும்!
                 👉 உங்களால் முடிந்தவரை நெருக்கமாக எடுத்துக் கொள்ளுங்கள்."""
#############################################################################################
eng_info = """Name: BUNCHY_TOP 
            Bunchy top is a viral disease caused by the Banana bunchy top virus (BBTV). 
            The disease, often called BBTD for banana bunchy top disease, 
            gets its name from the bunchy appearance of infected plants."""


eng_BUNCHY_TOP = """Name: BUNCHY_TOP.  Bunchy top is a viral disease caused by the Banana bunchy top virus (BBTV). 
The disease, often called BBTD for banana bunchy top disease,gets its name from the bunchy appearance of infected plants.
By that time, however, the  virus has most likely been spread to other plants by the banana aphid, Pentalonia nigronervosa.
Infected plants cannot recover and will serve as a source of viral particles unless they are destroyed. The virus is also spread through infected planting material.
There are no known sources of resistance to the virus.  All cultivars are believed to be susceptible. To the extent their reaction varies, 
it's in the time taken for the symptoms to develop. Bunchy top is considered to be the most devastating viral disease affecting bananas. 
The IUCN's Species Survival Commission has listed it among the world's 100 worst invasive alien species. ref: https://www.promusa.org/Bunchy+top"""

eng_CORDANA = """Name: Cordana leaf spot.  Cordana leaf spot is a disease of banana that, 
even though it is common worlwide, has generally little impact on production. 
It is caused by two Neocordana fungi that are often found as secondary invaders of leaf lesions caused by other fungi. 
Two Neocordana species are responsible for Cordana leaf spot symptoms: Neocordana musae, formerly Cordana musea, 
and originally described as Scoletrichum musae, and Neocordana johnstonii, formerly Cordana johnstonii, formerly Cordana johnstonii
which causes a disease very similar in appearance. Cordana leaf spot caused by N. musae is found in banana plantations all over the tropics.
Symptoms: The most characteristic symptoms of the disease are on the leaf.They are large, pale brown, oval to fusiform necrotic lesions with pale grey  concentric ring patterns, 
with a dark brown border surrounded by a bright yellow halo separating the lesion from the healthy leaf tissue,
Often, lesions coalesce into large necrotic patches. The leaves ultimately turn brown and  dry out. ref: https://www.promusa.org/Cordana+leaf+spot"""

eng_PANAMA = """Panama disease, also called banana wilt, a devastating disease of bananas caused by the soil-inhabiting fungus species Fusarium oxysporum forma specialis cubense.
A form of fusarium wilt, Panama disease is widespread throughout the tropics and can be found wherever susceptible banana cultivars are grown.
Notoriously difficult to control, the disease decimated global plantations of the Gros Michel banana in the 1950s and ’60s, which had dominated the commercial industry until its downfall. 
Its replacement, the modern Cavendish, has been threatened with a strain of the disease known as Tropical Race (TR) 4 since the 1990s; in 2019 TR 4 was confirmed in Colombia, 
marking the first appearance of the strain in the Americas. The Fusarium fungus invades young roots or root bases, often through wounds. Some infections progress into the rhizome (rootlike stem), 
followed by rapid invasion of the rootstock and leaf bases.
Ref: https://www.frontiersin.org/articles/10.3389/fpls.2019.01395/full"""

eng_SIGATOKA = """Sigatoka leaf spot (popularly known as Yellow Sigatoka) is a fungal disease caused by Pseudocercospora musicola (formerly Mycosphaerella musicola ). 
It was the first leaf spot disease to have a global impact on bananas but has since been  largely displaced by black leaf streak  in many banana production areas. 
However, it can still cause considerable losses at higher altitudes and cooler temperatures, 
and is also typically a greater problem during rainy seasons in subtropical banana growing regions . 
The disease reduces the leaf's photosynthetic capacity, which affects bunch size. It also shortens the fruit's green life, 
the time between harvest and ripening. Ref: https://www.promusa.org/Sigatoka+leaf+spot"""

##############################

mal_BUNCHY_TOP = """പേര്: കുറുനാമ്പ് രോഗം അഥവാ കുരുളടപ് . കുറുനാമ്പ് രോഗം അഥവാ കുരുളടപ്  വൈറസ് (ബിബിടിവി) മൂലമുണ്ടാകുന്ന ഒരു വൈറൽ രോഗമാണ് ബഞ്ചി ടോപ്പ് കുറുനാമ്പ് രോഗം അഥവാ കുരുളടപ് .
വാഴ കുലയുടെ മുകളിലെ രോഗത്തിന് BBTD എന്ന് വിളിക്കപ്പെടുന്ന ഈ രോഗത്തിന് രോഗബാധിതമായ ചെടികളുടെ കുലകളായി കാണപ്പെടുന്നതിൽ നിന്നാണ് ഈ പേര് ലഭിച്ചത്.
എന്നിരുന്നാലും, ആ സമയമായപ്പോഴേക്കും, പെന്റലോണിയ നൈഗ്രോനെർവോസ എന്ന വാഴപ്പഴം മുഖേന വൈറസ് മറ്റ് ചെടികളിലേക്കും വ്യാപിച്ചിരിക്കാം.
രോഗം ബാധിച്ച ചെടികൾക്ക് വീണ്ടെടുക്കാൻ കഴിയില്ല, അവ നശിപ്പിക്കപ്പെടാത്തപക്ഷം വൈറൽ കണങ്ങളുടെ ഉറവിടമായി വർത്തിക്കും. രോഗബാധയുള്ള നടീൽ വസ്തുക്കളിലൂടെയും വൈറസ് പടരുന്നു.
വൈറസിനെ പ്രതിരോധിക്കാൻ അറിയപ്പെടുന്ന ഉറവിടങ്ങളൊന്നുമില്ല. എല്ലാ ഇനങ്ങളും രോഗബാധിതരാണെന്ന് വിശ്വസിക്കപ്പെടുന്നു. അവരുടെ പ്രതികരണം എത്രത്തോളം വ്യത്യാസപ്പെടുന്നുവോ അത്രത്തോളം,
രോഗലക്ഷണങ്ങൾ വികസിക്കാൻ എടുക്കുന്ന സമയത്താണ് ഇത്. വാഴയെ ബാധിക്കുന്ന ഏറ്റവും വിനാശകരമായ വൈറൽ രോഗമായാണ് ബഞ്ചി ടോപ്പ് കണക്കാക്കപ്പെടുന്നത്.
IUCN-ന്റെ സ്പീഷീസ് സർവൈവൽ കമ്മീഷൻ ലോകത്തിലെ ഏറ്റവും മോശമായ 100 അന്യ ജീവികളുടെ പട്ടികയിൽ ഉൾപ്പെടുത്തിയിട്ടുണ്ട് Youtube: https://www.youtube.com/watch?v=PfwzGxhrdAM"""

mal_CORDANA = """പേര്: കോർഡാന ഇല പുള്ളി. വാഴയുടെ ഒരു രോഗമാണ് കോർഡാന ഇലപ്പുള്ളി,
ഇത് ലോകമെമ്പാടും സാധാരണമാണെങ്കിലും, ഉൽപ്പാദനത്തിൽ പൊതുവെ സ്വാധീനം കുറവാണ്.
രണ്ട് നിയോകോർഡാന ഫംഗസുകൾ മൂലമാണ് ഇത് സംഭവിക്കുന്നത്, അവ പലപ്പോഴും മറ്റ് ഫംഗസുകൾ മൂലമുണ്ടാകുന്ന ഇലകളുടെ മുറിവുകളുടെ ദ്വിതീയ ആക്രമണകാരികളായി കാണപ്പെടുന്നു.
രണ്ട് നിയോകോർഡാന സ്പീഷീസുകളാണ് കോർഡാന ഇലപ്പുള്ളി രോഗലക്ഷണങ്ങൾക്ക് ഉത്തരവാദികൾ: നിയോകോർഡാന മ്യൂസെ, മുമ്പ് കോർഡാന മ്യൂസിയം,
യഥാർത്ഥത്തിൽ സ്കോലെട്രിചം മ്യൂസെ, നിയോകോർഡാന ജോൺസ്റ്റോണി, മുമ്പ് കോർഡാന ജോൺസ്റ്റോണി, മുമ്പ് കോർഡാന ജോൺസ്റ്റോണി എന്നിങ്ങനെ വിവരിക്കപ്പെട്ടു
കാഴ്ചയിൽ വളരെ സമാനമായ ഒരു രോഗത്തിന് കാരണമാകുന്നു. ഉഷ്ണമേഖലാ പ്രദേശങ്ങളിലുടനീളമുള്ള വാഴത്തോട്ടങ്ങളിൽ എൻ മൂസ മൂലമുണ്ടാകുന്ന കോർഡാന ഇലപ്പുള്ളി കാണപ്പെടുന്നു.
രോഗലക്ഷണങ്ങൾ: രോഗത്തിന്റെ ഏറ്റവും സ്വഭാവഗുണമുള്ള ലക്ഷണങ്ങൾ ഇലയിലാണ്. അവ വലുതും ഇളം തവിട്ടുനിറമുള്ളതും ഓവൽ മുതൽ ഫ്യൂസിഫോം നെക്രോറ്റിക് നിഖേദ് വരെ ഇളം ചാരനിറത്തിലുള്ള കേന്ദ്രീകൃത വലയ പാറ്റേണുകളുമാണ്,
ഇരുണ്ട തവിട്ടുനിറത്തിലുള്ള ബോർഡർ, തിളങ്ങുന്ന മഞ്ഞ വലയത്താൽ ചുറ്റപ്പെട്ട, ആരോഗ്യമുള്ള ഇല കോശങ്ങളിൽ നിന്ന് മുറിവിനെ വേർതിരിക്കുന്നു,
പലപ്പോഴും, നിഖേദ് വലിയ നെക്രോറ്റിക് പാച്ചുകളായി കൂടിച്ചേരുന്നു. ഇലകൾ ആത്യന്തികമായി തവിട്ടുനിറമാവുകയും ഉണങ്ങുകയും ചെയ്യും. Ref: https://www.youtube.com/watch?v=ZyVeBRmIRFU"""

mal_PANAMA = """വാഴപ്പഴം വിൽറ്റ് എന്നും വിളിക്കപ്പെടുന്ന പനാമ രോഗം, മണ്ണിൽ വസിക്കുന്ന ഫംഗസ് ഇനം ഫ്യൂസാറിയം ഓക്സിസ്പോറം ഫോർമ സ്പെഷ്യലിസ് ക്യൂബൻസ് മൂലമുണ്ടാകുന്ന ഒരു വിനാശകരമായ രോഗമാണ്.
ഫ്യൂസാറിയം വിൽറ്റിന്റെ ഒരു രൂപമായ പനാമ രോഗം ഉഷ്ണമേഖലാ പ്രദേശങ്ങളിലുടനീളം വ്യാപകമാണ്.
നിയന്ത്രിക്കാൻ വളരെ ബുദ്ധിമുട്ടാണ്, ഈ രോഗം 1950 കളിലും 60 കളിലും ആഗോളതലത്തിൽ ഗ്രോസ് മൈക്കൽ വാഴയുടെ തോട്ടങ്ങളെ നശിപ്പിച്ചു, അത് അതിന്റെ തകർച്ച വരെ വാണിജ്യ വ്യവസായത്തിൽ ആധിപത്യം പുലർത്തി.
അതിന്റെ പകരക്കാരനായ ആധുനിക കാവൻഡിഷ്, 1990-കൾ മുതൽ ട്രോപ്പിക്കൽ റേസ് (TR) 4 എന്നറിയപ്പെടുന്ന ഒരു രോഗത്തിന്റെ ഭീഷണിയിലാണ്; 2019-ൽ കൊളംബിയയിൽ TR 4 സ്ഥിരീകരിച്ചു.
അമേരിക്കയിലെ സ്‌ട്രെയിനിന്റെ ആദ്യ രൂപം അടയാളപ്പെടുത്തുന്നു. ഫ്യൂസാറിയം ഫംഗസ് ഇളം വേരുകളിലോ വേരുകളുടെ അടിത്തറയിലോ ആക്രമിക്കുന്നു, പലപ്പോഴും മുറിവുകളിലൂടെ. ചില അണുബാധകൾ റൈസോമിലേക്ക് (വേരുപോലുള്ള തണ്ട്) പുരോഗമിക്കുന്നു.
തുടർന്ന് വേരുകൾ, ഇലകളുടെ അടിഭാഗം എന്നിവയുടെ ദ്രുത ആക്രമണം ഉണ്ടാവുന്നു.
Ref: https://www.manoramaonline.com/karshakasree/crop-info/2021/01/21/panama-disease-in-banana.html"""

mal_SIGATOKA = """സ്യൂഡോസെർകോസ്പോറ മ്യൂസിക്കോള (മുമ്പ് മൈകോസ്ഫെറല്ല മ്യൂസിക്കോള) മൂലമുണ്ടാകുന്ന ഒരു ഫംഗസ് രോഗമാണ് സിഗറ്റോക്ക ഇലപ്പുള്ളി (യെല്ലോ സിഗറ്റോക എന്നറിയപ്പെടുന്നത്).
വാഴപ്പഴത്തിൽ ആഗോളതലത്തിൽ സ്വാധീനം ചെലുത്തുന്ന ആദ്യത്തെ ഇലപ്പുള്ളി രോഗമായിരുന്നു ഇത്, പക്ഷേ പിന്നീട് പല വാഴ ഉൽപാദന മേഖലകളിലും കറുത്ത ഇല വരകളാൽ ഇത് മാറ്റിസ്ഥാപിക്കപ്പെട്ടു.
എന്നിരുന്നാലും, ഉയർന്ന ഉയരത്തിലും തണുത്ത താപനിലയിലും ഇത് ഇപ്പോഴും ഗണ്യമായ നഷ്ടം ഉണ്ടാക്കും.
കൂടാതെ ഉപ ഉഷ്ണമേഖലാ വാഴ വളരുന്ന പ്രദേശങ്ങളിൽ മഴക്കാലത്ത് ഇത് സാധാരണയായി ഒരു വലിയ പ്രശ്നമാണ്.
രോഗം ഇലയുടെ പ്രകാശസംശ്ലേഷണ ശേഷി കുറയ്ക്കുന്നു, ഇത് കുലയുടെ വലുപ്പത്തെ ബാധിക്കുന്നു. ഇത് പഴങ്ങളുടെ പച്ചയായ ആയുസ്സ് കുറയ്ക്കുകയും ചെയ്യുന്നു.
വിളവെടുപ്പിനും പാകമാകുന്നതിനും ഇടയിലുള്ള സമയം. Ref: https://www.youtube.com/watch?v=L3SfJal-nkA"""

########################################

hindi_BUNCHY_TOP = """(BUNCHY_TOP) पौधों के सभी हिस्सों को विकास के सभी चरणों पर वीषाणु प्रभावित कर सकता है। शुरुआती लक्षणों में डंठलों, मध्यशिराओं और नई पत्तियों के नीचे स्थित शिराओं पर गहरे हरे रंग की धारियां दिखाई देना शामिल हैं। बाद में, 
पत्ती की सतह (लेमिना) पर भी शिराओं के साथ इन छोटे गहरे हरे रंग के बिंदुओं और डैशों (जिसे मोर्स कोड स्वरूप कहा जाता है) को देखा जा सकता है। प्रभावित पत्तियाँ अविकसित, पतली और खड़ी हुई, और इनके किनारे घुंघराले और पर्णहरितहीन होते हैं जो गलना शुरू हो जाते हैं। गंभीर संक्रमणों में, 
नई पत्तियाँ में ये लक्षण अधिक बिगड़े हुए दिखाई देते हैं। मुकुट पर छोटी पीली हरी पत्तियाँ एकत्रित होकर "बंची टॉप" (गुच्छानुमा शीर्ष) का निर्माण करती हैं। समग्र विकास अवरुद्ध हो जाता है और हो सकता है कि पौधे गुच्छे या फल न पैदा कर पाएं। यदि फल उत्पन्न भी होते हैं, तो वे विकृत और छोटे रह जाते हैं। 
Ref: https://plantix.net/hi/library/plant-diseases/200020/bunchy-top-virus"""

hindi_CORDANA = """नाम: (CORDANA) कॉर्डाना लीफ स्पॉट। कोर्डाना लीफ स्पॉट केले का एक ऐसा रोग है जो,
भले ही यह दुनिया भर में आम है, लेकिन आम तौर पर उत्पादन पर इसका बहुत कम प्रभाव पड़ता है।
यह दो नियोकॉर्डाना कवक के कारण होता है जो अक्सर अन्य कवक के कारण पत्ती के घावों के द्वितीयक आक्रमणकारियों के रूप में पाए जाते हैं।
कॉर्डाना लीफ स्पॉट लक्षणों के लिए दो नियोकॉर्डाना प्रजातियां जिम्मेदार हैं: नियोकॉर्डाना मुसे, पूर्व में कॉर्डाना म्यूसिया,
और मूल रूप से स्कोलेट्रिचम मुसे, और नियोकॉर्डाना जॉनस्टोनी, पूर्व में कॉर्डाना जॉनस्टोनी, पूर्व में कॉर्डाना जॉनस्टोनी के रूप में वर्णित है
जो दिखने में बहुत ही समान बीमारी का कारण बनता है। एन. मुसा के कारण होने वाला कॉर्डाना लीफ स्पॉट सभी उष्णकटिबंधीय क्षेत्रों में केले के बागानों में पाया जाता है।
लक्षण: रोग के सबसे विशिष्ट लक्षण पत्ती पर होते हैं। वे बड़े, हल्के भूरे, अंडाकार से फ्यूसीफॉर्म नेक्रोटिक घावों के साथ हल्के भूरे रंग के गाढ़ा वलय पैटर्न के साथ होते हैं,
स्वस्थ पत्ती ऊतक से घाव को अलग करने वाले चमकीले पीले प्रभामंडल से घिरी एक गहरे भूरे रंग की सीमा के साथ,
अक्सर, घाव बड़े परिगलित पैच में जमा हो जाते हैं। पत्तियां अंततः भूरी हो जाती हैं और सूख जाती हैं। Ref: https://www.krishisewa.com/articles/disease-management/956-integrated-insect-and-disease-management-in-banana-crop.html"""

hindi_PANAMA = """(PANAMA) पनामा रोग, जिसे केले का मुरझाना भी कहा जाता है, मिट्टी में रहने वाली कवक प्रजाति फुसैरियम ऑक्सीस्पोरम फॉर्मा स्पेशलिस क्यूबेंस के कारण केले का एक विनाशकारी रोग है।
फुसैरियम विल्ट का एक रूप, पनामा रोग पूरे उष्ण कटिबंध में व्यापक है और जहां कहीं भी अतिसंवेदनशील केले की खेती की जाती है वहां पाया जा सकता है।
नियंत्रित करने के लिए कुख्यात रूप से कठिन, इस बीमारी ने 1950 और 60 के दशक में ग्रोस मिशेल केले के वैश्विक वृक्षारोपण को नष्ट कर दिया, जो अपने पतन तक वाणिज्यिक उद्योग पर हावी था।
इसके स्थान पर आधुनिक कैवेंडिश को 1990 के दशक से ट्रॉपिकल रेस (टीआर) 4 नामक बीमारी के एक तनाव से खतरा है; 2019 में कोलंबिया में TR 4 की पुष्टि हुई,
अमेरिका में तनाव की पहली उपस्थिति को चिह्नित करना। फुसैरियम कवक अक्सर घावों के माध्यम से युवा जड़ों या जड़ के आधार पर आक्रमण करता है। कुछ संक्रमण प्रकंद (जड़ जैसा तना) में आगे बढ़ते हैं,
इसके बाद रूटस्टॉक और लीफ बेस पर तेजी से आक्रमण हुआ। Ref:https://www.youtube.com/watch?v=gxlZTkKtU3s """

hindi_SIGATOKA = """सिगाटोका लीफ स्पॉट (जिसे येलो सिगाटोका के नाम से जाना जाता है) एक कवक रोग है जो स्यूडोसेर्कोस्पोरा म्यूजिकोला (पूर्व में माइकोस्फेरेला म्यूजिकोला) के कारण होता है।
केले पर वैश्विक प्रभाव डालने वाला यह पहला लीफ स्पॉट रोग था, लेकिन तब से कई केले उत्पादन क्षेत्रों में काली पत्ती की लकीर से विस्थापित हो गया है।
हालांकि, यह अभी भी उच्च ऊंचाई और ठंडे तापमान पर काफी नुकसान पहुंचा सकता है,
और आमतौर पर उपोष्णकटिबंधीय केला उगाने वाले क्षेत्रों में बरसात के मौसम में एक बड़ी समस्या होती है।
रोग पत्ती की प्रकाश संश्लेषक क्षमता को कम कर देता है, जो गुच्छों के आकार को प्रभावित करता है। यह फल के हरे जीवन को भी छोटा करता है,
फसल और पकने के बीच का समय। Ref: https://www.youtube.com/watch?v=BQncjjyToLI"""

#############################################

tamil_BUNCHY_TOP = """பெயர்: BUNCHY_TOP. பன்சி டாப் என்பது வாழைப்பழ பன்சி டாப் வைரஸால் (BBTV) ஏற்படும் ஒரு வைரஸ் நோயாகும்.
வாழை கொத்து மேல் நோய்க்கான BBTD என அழைக்கப்படும் இந்நோய், பாதிக்கப்பட்ட தாவரங்களின் கொத்து தோற்றத்திலிருந்து அதன் பெயரைப் பெற்றது.
இருப்பினும், அந்த நேரத்தில், வாழை அசுவினி, பென்டலோனியா நிக்ரோனெர்வோசா மூலம் வைரஸ் மற்ற தாவரங்களுக்கு பரவுகிறது.
பாதிக்கப்பட்ட தாவரங்கள் மீட்க முடியாது மற்றும் அவை அழிக்கப்படாவிட்டால் வைரஸ் துகள்களின் ஆதாரமாக செயல்படும். பாதிக்கப்பட்ட நடவுப் பொருட்களின் மூலமும் வைரஸ் பரவுகிறது.
வைரஸுக்கு எதிர்ப்புத் தெரிவிக்கும் ஆதாரங்கள் எதுவும் இல்லை. அனைத்து சாகுபடிகளும் எளிதில் பாதிக்கப்படும் என்று நம்பப்படுகிறது. அவற்றின் எதிர்வினை மாறுபடும் அளவிற்கு,
அறிகுறிகள் உருவாகும் நேரத்தில் இது உள்ளது. வாழைப்பழங்களை பாதிக்கும் மிக மோசமான வைரஸ் நோயாக பன்சி டாப் கருதப்படுகிறது.
IUCN இன் ஸ்பீசீஸ் சர்வைவல் கமிஷன், உலகின் மிக மோசமான 100 ஆக்கிரமிப்பு வேற்றுகிரக உயிரினங்களில் இதைப் பட்டியலிட்டுள்ளது.
Ref: https://ta.wiktionary.org/wiki/banana_bunchy_top_disease"""

tamil_CORDANA = """பெயர்: (CORDANA) கோர்டானா இலைப்புள்ளி. கோர்டானா இலைப்புள்ளி என்பது வாழையின் ஒரு நோயாகும்,
இது உலகளவில் பொதுவானதாக இருந்தாலும், உற்பத்தியில் பொதுவாக சிறிய தாக்கத்தை ஏற்படுத்துகிறது.
இது இரண்டு நியோகார்டானா பூஞ்சைகளால் ஏற்படுகிறது, அவை பெரும்பாலும் மற்ற பூஞ்சைகளால் ஏற்படும் இலை புண்களின் இரண்டாம் நிலை படையெடுப்பாளர்களாக காணப்படுகின்றன.
கோர்டானா இலைப்புள்ளி அறிகுறிகளுக்கு இரண்டு நியோகார்டானா இனங்கள் காரணம்: நியோகார்டானா மியூசே, முன்பு கோர்டானா மியூசியா,
மற்றும் முதலில் ஸ்கோலெட்ரிகம் மியூசே, மற்றும் நியோகார்டானா ஜான்ஸ்டோனி, முன்பு கோர்டானா ஜான்ஸ்டோனி, முன்பு கோர்டானா ஜான்ஸ்டோனி என விவரிக்கப்பட்டது
தோற்றத்தில் மிகவும் ஒத்த நோயை ஏற்படுத்துகிறது. N. மூசேயால் ஏற்படும் கோர்டானா இலைப்புள்ளி வெப்பமண்டலங்கள் முழுவதும் வாழைத் தோட்டங்களில் காணப்படுகிறது.
அறிகுறிகள்: நோயின் மிகவும் சிறப்பியல்பு அறிகுறிகள் இலையில் இருக்கும். அவை பெரிய, வெளிர் பழுப்பு, ஓவல் முதல் பியூசிஃபார்ம் நெக்ரோடிக் புண்கள் வெளிர் சாம்பல் செறிவு வளைய வடிவங்கள்,
ஆரோக்கியமான இலை திசுக்களில் இருந்து காயத்தை பிரிக்கும் ஒரு பிரகாசமான மஞ்சள் ஒளிவட்டத்தால் சூழப்பட்ட அடர் பழுப்பு நிற விளிம்புடன்,
பெரும்பாலும், புண்கள் பெரிய நெக்ரோடிக் திட்டுகளாக ஒன்றிணைகின்றன. இலைகள் இறுதியில் பழுப்பு நிறமாகி காய்ந்துவிடும்.
Ref: http://www.promusa.org/Cordana+leaf+spot"""

tamil_PANAMA = """(PANAMA) பனாமா நோய், வாழைப்பழ வில்ட் என்றும் அழைக்கப்படுகிறது, இது மண்ணில் வாழும் பூஞ்சை இனங்களான ஃபுசாரியம் ஆக்ஸிஸ்போரம் ஃபார்மா ஸ்பெஷலிஸ் க்யூபென்ஸால் ஏற்படும் வாழைப்பழத்தின் பேரழிவு நோயாகும்.
ஃபுசேரியம் வில்ட்டின் ஒரு வகை, பனாமா நோய் வெப்பமண்டலங்கள் முழுவதும் பரவலாக உள்ளது மற்றும் எளிதில் பாதிக்கப்படக்கூடிய வாழை சாகுபடிகள் எங்கு வளர்க்கப்படுகின்றன என்பதைக் காணலாம்.
1950கள் மற்றும் 60களில் க்ரோஸ் மைக்கேல் வாழைப்பழத்தின் உலகளாவிய தோட்டங்களை இந்த நோய் கட்டுப்படுத்துவது கடினமாக இருந்தது, அது வீழ்ச்சியடையும் வரை வணிகத் துறையில் ஆதிக்கம் செலுத்தியது.
அதன் மாற்றாக, நவீன கேவென்டிஷ், 1990களில் இருந்து ட்ராபிகல் ரேஸ் (டிஆர்) 4 எனப்படும் நோயின் திரிபுகளால் அச்சுறுத்தப்பட்டது; 2019 இல் TR 4 கொலம்பியாவில் உறுதி செய்யப்பட்டது.
அமெரிக்காவில் திரிபு முதல் தோற்றத்தை குறிக்கிறது. Fusarium பூஞ்சை இளம் வேர்கள் அல்லது வேர் தளங்களை அடிக்கடி காயங்கள் மூலம் படையெடுக்கிறது. சில நோய்த்தொற்றுகள் வேர்த்தண்டுக்கிழங்கில் (வேர் போன்ற தண்டு) முன்னேறும்.
அதைத் தொடர்ந்து ஆணிவேர் மற்றும் இலைத் தளங்களின் விரைவான படையெடுப்பு.
Ref: https://www.youtube.com/watch?v=_d0ufAAuhVc"""

tamil_SIGATOKA = """(SIGATOKA) சிகடோகா இலைப்புள்ளி (மஞ்சள் சிகடோகா என்று பிரபலமாக அறியப்படுகிறது) என்பது சூடோசெர்கோஸ்போரா மியூசிகோலா (முன்னர் மைக்கோஸ்பேரெல்லா மியூசிகோலா) மூலம் ஏற்படும் ஒரு பூஞ்சை நோயாகும்.
வாழைப்பழங்களில் உலகளாவிய தாக்கத்தை ஏற்படுத்திய முதல் இலைப்புள்ளி நோய் இதுவாகும், ஆனால் பல வாழை உற்பத்திப் பகுதிகளில் கருப்பு இலைக் கோடுகளால் பெருமளவில் இடம்பெயர்ந்துள்ளது.
இருப்பினும், அதிக உயரம் மற்றும் குளிர்ந்த வெப்பநிலையில் இது இன்னும் கணிசமான இழப்புகளை ஏற்படுத்தும்.
மேலும் பொதுவாக துணை வெப்பமண்டல வாழை வளரும் பகுதிகளில் மழைக்காலங்களில் இது ஒரு பெரிய பிரச்சனையாகும்.
இந்த நோய் இலையின் ஒளிச்சேர்க்கை திறனைக் குறைக்கிறது, இது கொத்து அளவை பாதிக்கிறது. இது பழத்தின் பசுமையான வாழ்க்கையையும் குறைக்கிறது.
அறுவடைக்கும் பழுக்க வைப்பதற்கும் இடைப்பட்ட காலம்.
Ref: https://www.youtube.com/watch?v=zGOEUliJNhI"""


def savejson(wa_id, lang):
    with open("data.json", encoding='utf-8', errors='ignore') as f:
        data_to_write = json.load(f)
        data_to_write[wa_id] = lang
        json.dump(data_to_write, open("data.json", "w"), indent = 4)



def sendtext(wa_id,text):
    client = Client(account_sid, auth_token)
    with open("data.json", encoding='utf-8', errors='ignore') as f:
        data = json.load(f)
        json.dump(data, open("data.json", "w"), indent = 4)
        lang_pref = data[wa_id]
        final_ans = lang_pref+text
    message = client.messages.create(
                            body=eval(final_ans), 
                            from_='whatsapp:+14155238886',
                            to=wa_id)
    print(message.sid)
    return message.sid       



class_names = {
    0 : 'BUNCHY_TOP',
    1 : 'CORDANA',
    2 : 'PANAMA',
    3 : 'SIGATOKA'
}



def conver_flow(msg,wa_id):
    list_quey = ['Hi', 'Hello', 'Hola', 'How are you', 'hi', 'hello', 'hola']
    lang_select = ['1', '2', '3', '4']
    if msg in list_quey:
        return """ Please select your language: 
                   1. English 
                   2. മലയാളം
                   3. हिन्दी
                   4. தமிழ் """
    elif msg == '1':
        #db.testwhats.insert_one({'wa_id': wa_id, 'greet': "eng_greet"})
        #db.testwhats.replace_one({'wa_id': wa_id, 'greet': "eng_greet"},{'wa_id' : wa_id}, upsert=True)
        resp = make_response(eng_greet)
        resp.set_cookie('greet', "eng_")
        savejson(wa_id, "eng_")
        return resp
    elif msg == '2':
        #db.testwhats.replace_one({'wa_id': wa_id, 'greet': "mal_greet"},{'wa_id' : wa_id}, upsert=True)
        resp = make_response(mal_greet)
        resp.set_cookie('greet', "mal_")
        savejson(wa_id, "mal_")
        return resp
    elif msg == '3':
        #db.testwhats.replace_one({'wa_id': wa_id, 'greet': "hindi_greet"},{'wa_id' : wa_id}, upsert=True)
        resp = make_response(hindi_greet)
        resp.set_cookie('greet', "hindi_")
        savejson(wa_id, "hindi_")
        return resp
    elif msg == '4':
        #db.testwhats.update_one({'wa_id': wa_id}, {"$set": {'greet': "tamil_greet"}})
        resp = make_response(tamil_greet)
        resp.set_cookie('greet', "tamil_")
        savejson(wa_id, "tamil_")
        return resp                
    return "please send a valid message"  

def imgdraw(path):
    path_to_folder = 'C:/Users/lenovo/Pictures/Disease_dataset/app/src'
    img1 = cv2.imread(os.path.join(path_to_folder, path+".jpg"))
    img_building = cv2.cvtColor(img1, cv2.COLOR_BGR2RGB)  # Convert from cv's BRG default color order to RGB
    orb = cv2.ORB_create()
    key_points, description = orb.detectAndCompute(img_building, None)
    img_building_keypoints = cv2.drawKeypoints(img_building, 
                                            key_points, 
                                            img_building, 
                                            flags=cv2.DRAW_MATCHES_FLAGS_DRAW_RICH_KEYPOINTS)
    final_img = cv2.resize(img_building_keypoints, (1000,650))
    cv2.imwrite('C:/Users/lenovo/Pictures/Disease_dataset/app/cv/'+path+".jpg", final_img)



def prediction(path):
    print("Please wait...")
    img = load_img(path, target_size= (256,256))
    i = img_to_array(img)
    im = preprocess_input(i)
    img = np.expand_dims(im, axis= 0)
    print(model.predict(img))
    pred = np.argmax(model.predict(img))
    return pred
#     print(f"result of your file is {pred}")



def urltofile(url):
    filename = url.split("/")[-1].split("?")[0]
    filter_file_name = re.sub('[^A-Za-z0-9]+', '', filename)
    fullfilename = os.path.join("src", filter_file_name+".jpg")
    f = open(fullfilename,'wb')
    r = requests.head(url, allow_redirects=True)
    f.write(urllib.request.urlopen(r.url).read())
    f.close()
    # urllib.request.urlretrieve(url, fullfilename)  
    # r = requests.head(url, allow_redirects=True)
    # print(r.url)
    # y = threading.Thread(target = imgdraw, args = (filter_file_name,))
    # y.start()
    path = fullfilename
    return prediction(path)


def threadmain_full_context(wa_id,url):
    prediction = urltofile(url)
    final_pred = class_names[prediction]
    result = sendtext(wa_id,final_pred)
    return result



@app.route('/api', methods=['GET', 'POST'])
def apifromserver():
    key = request.args.get('key')
    api_key = {}
    if key == api_key:
        from_number = request.form['From']
        message = request.form['Body']
        try:
            headers={ 'content-type':'text/plain'}
            media = request.form['MediaUrl0']
            print(media)
            #result = urltofile(media)
            #from_db_data = db.testwhats.find_one({"wa_id": from_number})
            from_db_data = request.cookies.get('greet')
            if from_db_data is None:
                reply_back = conver_flow(message,from_number)
            else:
                from_db_data = request.cookies.get('greet')
                if from_db_data == "eng_":
                    x = threading.Thread(target = threadmain_full_context, args = (from_number, media))
                    x.start()
                    return "Please wait a second. we analizing your photo!", headers
                elif from_db_data == "mal_":
                    x = threading.Thread(target = threadmain_full_context, args = (from_number, media))
                    x.start()
                    return "ദയവായി ഒരു നിമിഷം കാത്തിരിക്കൂ. ഞങ്ങൾ നിങ്ങളുടെ ഫോട്ടോ വിശകലനം ചെയ്യുന്നു!", headers
                elif from_db_data == "hindi_":
                    x = threading.Thread(target = threadmain_full_context, args = (from_number, media))
                    x.start()
                    return "कृपया एक सेकंड प्रतीक्षा करें। हम आपकी तस्वीर का विश्लेषण कर रहे हैं!", headers
                elif from_db_data == "tamil_":
                    x = threading.Thread(target = threadmain_full_context, args = (from_number, media))
                    x.start()
                    return "தயவு செய்து சிறிது நேரம் காத்திருக்கவும். உங்கள் புகைப்படத்தை நாங்கள் பகுப்பாய்வு செய்கிறோம்!", headers     
            return reply_back, headers

        except:
            print('no media message')    
            reply_back = conver_flow(message,from_number)
        #db.testwhats.insert_one({'id_num': request.form['WaId'], 'body': "todo body"})
        print(from_number,message)
        headers={ 'content-type':'text/plain'}
        return reply_back, headers
    return 'api-key not accessable!'       
             


@app.route('/message', methods=['GET', 'POST'])
def message_classify():
    text = request.args.get('text')
    return conver_flow(text)



#Route method "save file" which is download all file from url. 
# @app.route('/savefile')
# def urltofile():
#     url = request.args.get('url')
#     filename = url.split("/")[-1].split("?")[0]
#     filter_file_name = re.sub('[^A-Za-z0-9]+', '', filename)
#     fullfilename = os.path.join("src", filter_file_name+".jpg")
#     f = open(fullfilename,'wb')
#     r = requests.head(url, allow_redirects=True)
#     f.write(urllib.request.urlopen(r.url).read())
#     f.close()
#     # urllib.request.urlretrieve(url, fullfilename)  
#     # r = requests.head(url, allow_redirects=True)
#     # print(r.url)

#     # path = fullfilename
#     # prediction(path)
#     return 'Hello, World!'


 
if __name__ == '__main__':
 app.run(host='0.0.0.0', debug=True)