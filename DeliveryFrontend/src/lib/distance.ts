const distance = (
    latitude1 : number,
    longitude1 : number,
    latitude2 : number,
    longitude2 : number
) : number => {
    const latitude1_radian : number = (Math.PI * latitude1) / 180;
    const latitude2_radian : number = (Math.PI * latitude2) / 180;
    const delta_lat_radian : number = ((latitude1 - latitude2) * Math.PI) / 180;
    const delta_lon_radian : number = ((longitude1 - longitude2) * Math.PI) / 180;

    const a : number = Math.pow(Math.sin(delta_lat_radian / 2), 2) + 
                        Math.cos(latitude1_radian) * Math.cos(latitude2_radian) *
                        Math.pow(Math.sin(delta_lon_radian / 2), 2);

    const c : number = 2 * Math.atan2(Math.sqrt(a), Math.sqrt(1 - a));

    return 6371 * c;
}
 
export default distance;