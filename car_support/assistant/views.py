import speech_recognition as sr
import pyttsx3
from django.shortcuts import render
from django.http import JsonResponse
import wikipediaapi  # Import Wikipedia API

# Initialize Wikipedia API with a user agent
wiki = wikipediaapi.Wikipedia(language='en', user_agent="MyPythonApp/1.0 (http://example.com)")


def get_wikipedia_summary(topic):
    page = wiki.page(topic)
    if page.exists():
        return page.summary
    else:
        return "No detailed information found for this topic on Wikipedia."


# Initialize Text-to-Speech Engine
engine = pyttsx3.init()

# Car Support Info
car_info = {
    "oil change": (
        "For optimal performance, change engine oil every 5,000-7,500 kilometers. "
        "Regular oil changes help keep the engine clean and lubricated, preventing damage and improving fuel efficiency."
    ),
    "battery check": (
        "Inspect the car battery terminals regularly for any corrosion. A healthy battery should last "
        "between 3-5 years. If you notice slow engine crank, dim headlights, or electrical issues, it might "
        "be time to replace the battery. Keep the terminals clean and securely fastened."
    ),
    "tire pressure": (
        "Maintain the recommended tire pressure, usually between 30-35 PSI (2.1-2.4 Bar). Proper tire pressure ensures "
        "better fuel efficiency, improved handling, and longer tire life. Check tire pressure monthly and before "
        "long trips. Don't forget to check the spare tire!"
    ),
    "brake issues": (
        "If your brakes feel soft or make noise, it's crucial to check the brake fluid and pads. Squeaking or grinding "
        "noises indicate that the brake pads may be worn out. Regular maintenance of the braking system ensures your "
        "safety on the road."
    ),
    "engine trouble": (
        "If the check engine light comes on, inspect components like spark plugs, fuel filter, or oxygen sensor. "
        "These parts play a crucial role in engine performance. Ignoring engine issues can lead to more significant "
        "problems down the road."
    ),
    "emergency contacts": (
        "In case of a roadside emergency, always have the contact numbers for your car service provider, local towing service, "
        "and nearest police station handy. It's also beneficial to keep an emergency kit in your car that includes items like "
        "a first aid kit, flashlight, jumper cables, and reflective triangles."
    ),
    "scheduled maintenance": (
        "Regular scheduled maintenance is essential for prolonging the life of your vehicle. Follow the manufacturer's "
        "recommendations for services such as fluid checks, air filter replacements, and timing belt changes. This helps "
        "catch potential issues early and keeps your car running smoothly."
    ),
    "fuel efficiency tips": (
        "To improve fuel efficiency, maintain a steady speed, avoid excessive idling, and ensure proper tire inflation. "
        "Removing unnecessary weight from the vehicle and using cruise control on highways can also contribute to better "
        "fuel economy."
    ),
    "air conditioner issues": (
        "If your car's air conditioner isn't blowing cold air, it may be due to low refrigerant levels, a faulty compressor, "
        "or a clogged condenser. Check the refrigerant levels and inspect the air conditioning system components."
    ),
    "transmission problems": (
        "If your car is having trouble shifting gears or making strange noises while shifting, it may be due to low transmission fluid, "
        "a worn clutch, or other internal transmission issues. Check the transmission fluid levels and consider getting a professional inspection."
    ),
    "alternator failure": (
        "If your car's electrical components are malfunctioning or the battery warning light is on, it may be due to a failing alternator. "
        "The alternator charges the battery and powers the electrical system while the engine is running. If you suspect an alternator issue, "
        "get it checked and replaced if necessary."
    ),
    "cooling system problems": (
        "If your car is overheating, it may be due to issues with the cooling system, such as a leaking radiator, a malfunctioning water pump, "
        "or a clogged coolant hose. Check the coolant levels and inspect the cooling system components."
    ),
    "suspension issues": (
        "If your car is experiencing a bumpy ride, uneven tire wear, or difficulty handling, it may be due to suspension issues. "
        "Check the shocks, struts, and other suspension components for wear and damage."
    ),
    "headlight problems": (
        "If your headlights are dim or not working, it may be due to a burned-out bulb, a faulty headlight switch, or an issue with the wiring. "
        "Inspect the headlights and replace any faulty components."
    ),
    "exhaust system issues": (
        "If your car is making loud noises or emitting unusual smells, it may be due to exhaust system issues. Check for leaks or damage in the exhaust "
        "pipes, muffler, and catalytic converter. A malfunctioning exhaust system can also affect engine performance and emissions."
    )
}


# Function to recognize speech and respond with text and speech
def recognize_speech():
    recognizer = sr.Recognizer()
    with sr.Microphone() as source:
        try:
            # Stop the existing run loop if any
            engine.stop()

            engine.say("Please speak your query, for example, Oil Change, Battery Check, or Tire Pressure.")
            engine.runAndWait()
            print("Listening...")
            audio = recognizer.listen(source)
            query = recognizer.recognize_google(audio).lower()
            print(f"Recognized: {query}")

            response = car_info.get(query, "Sorry, I couldn't understand that.")

            # Fetch detailed information from Wikipedia if basic info is not sufficient
            if response == "Sorry, I couldn't understand that.":
                response = get_wikipedia_summary(query)

            engine.say(response)
            engine.runAndWait()
            print(response)
            return response

        except sr.UnknownValueError:
            print("Could not understand your voice.")
            return "Could not understand your voice. Please try again."
        except sr.RequestError:
            print("Error accessing the voice recognition service.")
            return "Error accessing the voice recognition service."


# Django view for web-based response
def home(request):
    return render(request, 'assistant/home.html')


def get_voice_query(request):
    response = recognize_speech()
    return JsonResponse({"message": response})
