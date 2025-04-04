import {createClient, RealtimeChannel, SupabaseClient} from '@supabase/supabase-js';

const instance : SupabaseClient = createClient(
    import.meta.env.VITE_SUPABASE_URL!, 
    import.meta.env.VITE_SUPABASE_KEY!
);

let channel : RealtimeChannel | null = null;

export function getSignal (
    handler : any
) : RealtimeChannel {
    if(channel == null) {
        channel =  instance.
            channel('schema-db-changes')
            .on(
                'postgres_changes',
                {
                    event : "UPDATE",
                    schema : 'public',
                    table : "order_queue"
                },
                (payload) => {
                    console.log(payload);
                    handler(payload.new.id);
                }
            )
            .subscribe();        
    }

    return channel;
}