// Constants
const ORDER_LINK = "https://t.me/indicare_uz";
const TELEGRAM_LINK = "t.me/indicareuz";
const INSTAGRAM_LINK = "https://www.instagram.com/indicare.uz/";
const UZUM_LINK = "https://uzum.uz/uz/shop/indicareuz";

// Allowed user IDs
const allowed_user_ids = new Set([
    '+821025321434', 'Dina', 'Dinora', // Dinora
    'shbobur2', 'Bobur',               // Bobur
    '+998971451106', 'Indira',         // Indira
    'indicare_uz'                      // Indicare account
]);

// Footer designs - you can assign any of these to FOOTER
const FOOTER_DESIGNS = {
    // Current design
    default: "\n\n✨ [Buyurtma qiling]({order_link})! ✨\n\n🛍️ [Uzum]({uzum_link}) | 📲 [Telegram]({telegram_link}) | 📷 [Instagram]({instagram_link})",
    
    // Minimalist design
    minimal: "\n\n[Buyurtma]({order_link}) • [Uzum]({uzum_link}) • [TG]({telegram_link}) • [IG]({instagram_link})",
    
    // Vertical design with emojis
    vertical: "\n\n✨ [Buyurtma qiling]({order_link})! ✨\n\n🛍️ [Uzum]({uzum_link})\n📲 [Telegram]({telegram_link})\n📷 [Instagram]({instagram_link})",
    
    // Decorative design
    decorative: "\n\n⭐️━━━━━━━━━━━━━━━━━━━━━⭐️\n[💫 Buyurtma qiling]({order_link})\n\n[🎁 Uzum]({uzum_link})\n[📱 Telegram]({telegram_link})\n[📸 Instagram]({instagram_link})\n⭐️━━━━━━━━━━━━━━━━━━━━━⭐️",
    
    // Modern compact design
    modern: "\n\n🌟 [Order Now]({order_link})\n━━━━━━━━━\n[Uzum]({uzum_link}) ⋄ [TG]({telegram_link}) ⋄ [IG]({instagram_link})",
    
    // Branded design
    branded: "\n\n✦ INDICARE ✦\n[Buyurtma qiling]({order_link})\n\n[Uzum]({uzum_link}) • [Telegram]({telegram_link}) • [Instagram]({instagram_link})\n✦ ━━━━━━ ✦"
};

// Footer template - To test different designs, assign any design from FOOTER_DESIGNS
// Example: const FOOTER = FOOTER_DESIGNS.vertical;
const FOOTER = FOOTER_DESIGNS.branded;

// Format the footer with the constants
function formatFooter() {
    return FOOTER
        .replace("{order_link}", ORDER_LINK)
        .replace("{telegram_link}", TELEGRAM_LINK)
        .replace("{instagram_link}", INSTAGRAM_LINK)
        .replace("{uzum_link}", UZUM_LINK);
}

// Handle incoming requests
export default {
    async fetch(request, env, ctx) {
        if (request.method === "POST") {
            const payload = await request.json();

            // Check if the payload contains a message
            if ('message' in payload) {
                const chatId = payload.message.chat.id;
                const userId = payload.message.from.username || payload.message.from.first_name;

                // Check if the user is allowed
                if (allowed_user_ids.has(userId)) {
                    let messageText = payload.message.text || payload.message.caption || "No caption or text provided.";
                    const footer = formatFooter();
                    const finalMessage = `${messageText}${footer}`;

                    // Check if the message contains a photo
                    if (payload.message.photo) {
                        // Get the largest available photo file_id
                        const photoFileId = payload.message.photo[payload.message.photo.length - 1].file_id;

                        console.log('hmm, photo, should be ok!');

                        // Send the photo with the formatted caption
                        const photoUrl = `https://api.telegram.org/bot${env.API_KEY}/sendPhoto?chat_id=${chatId}&photo=${photoFileId}&caption=${encodeURIComponent(finalMessage)}&parse_mode=Markdown`;
                        await fetch(photoUrl);
                    } else {
                        console.log('text, should be ok!');

                        // If no photo, send only the formatted message
                        const textUrl = `https://api.telegram.org/bot${env.API_KEY}/sendMessage?chat_id=${chatId}&text=${encodeURIComponent(finalMessage)}&parse_mode=Markdown`;
                        await fetch(textUrl);
                    }
                } else {
                    // Reject unauthorized users
                    const rejectMessage = "You are not authorized to use this bot.";
                    const rejectUrl = `https://api.telegram.org/bot${env.API_KEY}/sendMessage?chat_id=${chatId}&text=${encodeURIComponent(rejectMessage)}`;
                    await fetch(rejectUrl);
                }
            }
        }

        // Return a response (required by Cloudflare Workers)
        return new Response("OK");
    }
}