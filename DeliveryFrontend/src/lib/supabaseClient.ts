import {createClient, RealtimeChannel, RealtimePostgresInsertPayload, SupabaseClient} from '@supabase/supabase-js';

const instance : SupabaseClient = createClient(
    import.meta.env.VITE_SUPABASE_URL!, 
    import.meta.env.VITE_SUPABASE_KEY!
);

let channel : RealtimeChannel | null = null;

export function subscribeChannel (
    tableName : Readonly<string>,
    onInsert : any,
    onUpdate : any
) : RealtimeChannel {
    if(channel == null) {
        channel =  instance.
            channel('schema-db-changes')
            .on(
                'postgres_changes',
                {
                    event : "INSERT",
                    schema : 'public',
                    table : tableName
                },
                (payload) => {
                    onInsert(payload);
                }
            )
            .on(
                'postgres_changes',
                {
                    event : 'UPDATE',
                    schema : 'public',
                    table : tableName
                },
                (payload) => {
                    onUpdate(payload);
                }
            )
            .subscribe();        
    }

    return channel;
}

export function removeChannel (channel : RealtimeChannel) {
    instance.removeChannel(channel);
}