Texture2D src : register(t0);

cbuffer constant0 : register(b0) {
    float scale;
};

float4 ColorReduction(float4 pos : SV_Position) : SV_Target {
    float4 c= src.Load(int3(pos.xy, 0));
    float4 cadd = round(c * scale) / scale ;
    return float4(cadd);
}