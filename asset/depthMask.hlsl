Texture2D src : register(t0);
Texture2D src2 : register(t1);

cbuffer constant0 : register(b0) {
    float border;
    float blur;
};

float4 depthMask(float4 pos : SV_Position) : SV_Target {
    float4 c= src.Load(int3(pos.xy, 0));
    float4 c2= src2.Load(int3(pos.xy, 0));
    float bVal = c.rgb.r /3;
    float diff = bVal - border ;
    float4 ret;
    
    if (diff > 0){
        ret = float4(c2.rgb , 1);
    }
    else{
        ret = 0;
    }
    return float4(ret);
}