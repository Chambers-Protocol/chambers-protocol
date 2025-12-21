// PATH: supabase/functions/stripe-webhook/index.ts
import { serve } from "https://deno.land/std@0.168.0/http/server.ts";
import { createClient } from "https://esm.sh/@supabase/supabase-js@2";
import { Resend } from "https://esm.sh/resend@2.0.0";
import Stripe from "https://esm.sh/stripe@12.0.0";

// INITALIZE CONNECTIONS
const stripe = new Stripe(Deno.env.get("STRIPE_SECRET_KEY") || "", {
  apiVersion: "2022-11-15",
  httpClient: Stripe.createFetchHttpClient(),
});
const resend = new Resend(Deno.env.get("RESEND_API_KEY"));
const supabase = createClient(
  Deno.env.get("SUPABASE_URL") ?? "",
  Deno.env.get("SUPABASE_SERVICE_ROLE_KEY") ?? ""
);

serve(async (req) => {
  const signature = req.headers.get("Stripe-Signature");

  try {
    // 1. READ THE STRIPE PAYLOAD
    const body = await req.text();
    const webhookSecret = Deno.env.get("STRIPE_WEBHOOK_SECRET");
    
    // 2. VERIFY SECURITY SIGNATURE (Prevents Hackers faking payments)
    let event;
    try {
      event = await stripe.webhooks.constructEventAsync(body, signature!, webhookSecret!);
    } catch (err) {
      return new Response(`Webhook Error: ${err.message}`, { status: 400 });
    }

    // 3. PROCESS THE PAYMENT
    if (event.type === "checkout.session.completed") {
      const session = event.data.object;
      const customerEmail = session.customer_details?.email;

      if (!customerEmail) {
        throw new Error("No email found in transaction");
      }

      // 4. MINT THE KEY (The Product)
      // We generate a secure random string: "chambers_sk_..."
      const newApiKey = `chambers_sk_${crypto.randomUUID().replace(/-/g, "")}`;
      
      console.log(`[MINTING] Generating key for ${customerEmail}`);

      // 5. DEPOSIT TO VAULT (Supabase)
      const { error: dbError } = await supabase
        .from("api_keys")
        .insert({
          client_email: customerEmail,
          api_key_hash: newApiKey, // Storing raw for MVP, Hash in v2
          credits_remaining: 1000000, // 1 Million Entropy Credits
          is_active: true
        });

      if (dbError) {
        console.error("Database Error:", dbError);
        return new Response("Database Write Failed", { status: 500 });
      }

      // 6. DELIVER VIA COURIER (Resend Email)
      await resend.emails.send({
        from: "Chambers Protocol <system@protocol.theeinsteinbridge.com>", // Update this domain later
        to: [customerEmail],
        subject: "ACCESS GRANTED: Chambers Protocol API Key",
        html: `
          <div style="font-family: monospace; padding: 20px; background: #f4f4f4;">
            <h2>// PROTOCOL ACTIVATED</h2>
            <p>Payment confirmed. Your node is funded.</p>
            <hr/>
            <p><strong>API KEY:</strong></p>
            <h3 style="background: #000; color: #0f0; padding: 10px; display: inline-block;">${newApiKey}</h3>
            <p><strong>CREDITS:</strong> 1,000,000</p>
            <hr/>
            <p>1. Add this key to your local <code>.env</code> file: <code>CHAMBERS_API_KEY=...</code></p>
            <p>2. Restart your MCP server.</p>
            <p><em>The Einstein Bridge</em></p>
          </div>
        `,
      });

      return new Response(JSON.stringify({ received: true }), {
        headers: { "Content-Type": "application/json" },
      });
    }

    return new Response("Event Ignored (Not Checkout)", { status: 200 });

  } catch (err) {
    console.error(err);
    return new Response(`Server Error: ${err.message}`, { status: 500 });
  }
});