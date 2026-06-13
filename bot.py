from telegram import Update
from telegram.ext import ApplicationBuilder, CommandHandler, ContextTypes

TOKEN = "8868701435:AAHTWf6b5wvmP3wN1qlFClFC6ycs7dMrmNs"

inventario = {
    1: {"nombre": "Peras", "precio": 4000, "cantidad": 65, "cantidad_inicial": 65},
    2: {"nombre": "Limones", "precio": 1500, "cantidad": 25, "cantidad_inicial": 25},
    3: {"nombre": "Moras", "precio": 2000, "cantidad": 30, "cantidad_inicial": 30},
    4: {"nombre": "Piñas", "precio": 3000, "cantidad": 15, "cantidad_inicial": 15},
    5: {"nombre": "Tomates", "precio": 1000, "cantidad": 30, "cantidad_inicial": 30},
    6: {"nombre": "Fresas", "precio": 3000, "cantidad": 12, "cantidad_inicial": 12},
    7: {"nombre": "Frunas", "precio": 300, "cantidad": 50, "cantidad_inicial": 50},
    8: {"nombre": "Galletas", "precio": 500, "cantidad": 400, "cantidad_inicial": 400},
    9: {"nombre": "Chocolates", "precio": 1200, "cantidad": 500, "cantidad_inicial": 500},
    10: {"nombre": "Arroz", "precio": 1200, "cantidad": 60, "cantidad_inicial": 60},
}

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text(
        "🛒 Bienvenida Doña Rosa!\n\n"
        "Comandos disponibles:\n"
        "/inventario - Ver todos los productos\n"
        "/insertar <nombre> <precio> <cantidad> - Agregar producto\n"
        "/actualizar <id> <cantidad> - Actualizar cantidad\n"
        "/borrar <id> - Borrar producto\n"
        "/costototal - Ver costo total del inventario\n"
        "/alertas - Ver productos por agotarse"
    )

async def inventario_cmd(update: Update, context: ContextTypes.DEFAULT_TYPE):
    msg = "📦 *Inventario:*\n\n"
    for id, p in inventario.items():
        msg += f"{id}. {p['nombre']} - ${p['precio']} - Cantidad: {p['cantidad']}\n"
    await update.message.reply_text(msg, parse_mode="Markdown")

async def insertar(update: Update, context: ContextTypes.DEFAULT_TYPE):
    try:
        nombre = context.args[0]
        precio = int(context.args[1])
        cantidad = int(context.args[2])
        nuevo_id = max(inventario.keys()) + 1
        inventario[nuevo_id] = {"nombre": nombre, "precio": precio, "cantidad": cantidad, "cantidad_inicial": cantidad}
        await update.message.reply_text(f"✅ Producto '{nombre}' agregado con ID {nuevo_id}")
    except:
        await update.message.reply_text("❌ Uso correcto: /insertar <nombre> <precio> <cantidad>")

async def actualizar(update: Update, context: ContextTypes.DEFAULT_TYPE):
    try:
        id = int(context.args[0])
        cantidad = int(context.args[1])
        if id in inventario:
            inventario[id]["cantidad"] = cantidad
            p = inventario[id]
            alerta = ""
            if cantidad <= p["cantidad_inicial"] * 0.10:
                alerta = f"\n⚠️ ALERTA: {p['nombre']} está por agotarse!"
            await update.message.reply_text(f"✅ {p['nombre']} actualizado a {cantidad} unidades{alerta}")
        else:
            await update.message.reply_text("❌ ID no encontrado")
    except:
        await update.message.reply_text("❌ Uso correcto: /actualizar <id> <cantidad>")

async def borrar(update: Update, context: ContextTypes.DEFAULT_TYPE):
    try:
        id = int(context.args[0])
        if id in inventario:
            nombre = inventario[id]["nombre"]
            del inventario[id]
            await update.message.reply_text(f"✅ Producto '{nombre}' eliminado")
        else:
            await update.message.reply_text("❌ ID no encontrado")
    except:
        await update.message.reply_text("❌ Uso correcto: /borrar <id>")

async def costo_total(update: Update, context: ContextTypes.DEFAULT_TYPE):
    total = sum(p["precio"] * p["cantidad"] for p in inventario.values())
    await update.message.reply_text(f"💰 Costo total del inventario: ${total:,}")

async def alertas(update: Update, context: ContextTypes.DEFAULT_TYPE):
    msg = "⚠️ *Productos por agotarse (menos del 10%):*\n\n"
    encontrados = False
    for id, p in inventario.items():
        if p["cantidad"] <= p["cantidad_inicial"] * 0.10:
            msg += f"- {p['nombre']}: {p['cantidad']} unidades\n"
            encontrados = True
    if not encontrados:
        msg = "✅ Todos los productos tienen stock suficiente"
    await update.message.reply_text(msg, parse_mode="Markdown")

if __name__ == "__main__":
    app = ApplicationBuilder().token(TOKEN).build()
    app.add_handler(CommandHandler("start", start))
    app.add_handler(CommandHandler("inventario", inventario_cmd))
    app.add_handler(CommandHandler("insertar", insertar))
    app.add_handler(CommandHandler("actualizar", actualizar))
    app.add_handler(CommandHandler("borrar", borrar))
    app.add_handler(CommandHandler("costototal", costo_total))
    app.add_handler(CommandHandler("alertas", alertas))
    print("Bot corriendo...")
    app.run_polling()