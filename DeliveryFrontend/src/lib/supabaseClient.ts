import {createClient, RealtimeChannel, SupabaseClient} from '@supabase/supabase-js';
import apiFetcher from './apiFetcher';

const instance : SupabaseClient = createClient(
    import.meta.env.VITE_SUPABASE_URL!, 
    import.meta.env.VITE_SUPABASE_KEY!
);

let channel : RealtimeChannel | null = null;

export function sendSignal(
    orderId : number
) {
    return apiFetcher.deliverySignal(orderId);
}

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


export function deliveryChannelSubscription (
    orderQueueHandler : any,
    orderToDeliveryHandler : any,
    orderToShopHandler : any
) : RealtimeChannel {
    return instance.
        channel('schema-db-changes')
        .on(
            'postgres_changes',
            {
                event : "UPDATE",
                schema : 'public',
                table : "order_queue"
            },
            (payload) => {
                orderQueueHandler(payload);
            }
        )
        .on(
            'postgres_changes',
            {
                event : '*',
                schema : 'public',
                table : "order_to_delivery"
            },
            (payload) => {
                orderToDeliveryHandler(payload);
            }
        )
        .on(
            'postgres_changes',
            {
                event : '*',
                schema : 'public',
                table : "order_to_shop"
            },
            (payload) => {
                orderToShopHandler(payload);
            }
        )
        .subscribe();        
}

export async function getOrderLocation(orderId : number) {
    const { data } =  await instance
        .from('order_queue')
        .select('latitude, longitude')
        .eq('id', orderId)
        .single();

    return {
        latitude : data!.latitude as number,
        longitude : data!.longitude as number
    }
}

export function removeChannel (channel : RealtimeChannel) {
    instance.removeChannel(channel);
}