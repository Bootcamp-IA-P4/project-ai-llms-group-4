from app.generator import generate_text

if __name__ == "__main__":
    topic = input("¿Sobre qué tema quieres generar contenido? ")
    platform = input("¿Para qué plataforma es? (Blog, Twitter, etc.): ")

    prompt = f"Escribe un contenido atractivo para {platform} sobre: {topic}"
    result = generate_text(prompt)
    print("\n📝 Contenido generado:\n")
    print(result)
