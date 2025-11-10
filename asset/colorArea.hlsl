Texture2D src : register(t0);

cbuffer constant0 : register(b0) {
    float ro;
    float rh;
    float go;
    float gh;
    float bo;
    float bh;
    float ao;
    float ah;
};

float4 colorArea(float4 pos : SV_Position) : SV_Target {
    float4 gain = float4( rh + ah, gh + ah, bh + ah, 0) / 127.0 + 1;
    float4 offs = float4( ro + ao, go + ao, bo + ao, 0) / 127.0;
    float4 c= src.Load(int3(pos.xy, 0));
    float4 cadd = c * gain + offs;
    return float4(cadd);
}