# Memory Optimization Summary

## Memory Usage Analysis

### Baseline Memory (Tested Locally)
- **Total Memory**: ~229 MB
- **Breakdown**:
  - sentence-transformers model: ~216 MB
  - FAISS: ~20 MB
  - FastAPI/uvicorn: ~35 MB
  - pandas/dashboard_data: ~60 MB
  - Other: ~10 MB

### Render 512 MB Limit
- **Current Usage**: 229 MB (44.7% of limit)
- **Available**: 283 MB headroom

## Optimizations Applied

1. **Single Worker**: Set uvicorn to use `--workers 1` to prevent multiple processes
2. **Float32 Embeddings**: Ensured all embeddings use float32 instead of float64 (50% memory savings)
3. **Garbage Collection**: Added explicit GC calls after loading agent
4. **Context Limiting**: Limited context length to 3000 characters to prevent memory spikes
5. **Memory Monitoring**: Added `/api/health` endpoint to monitor memory usage

## If Still Running Out of Memory

### Option 1: Upgrade Render Plan
- Render offers plans with more memory (1GB, 2GB, etc.)

### Option 2: Further Optimizations
- Use a smaller embedding model (e.g., `all-MiniLM-L6-v2` is already small)
- Lazy load the model only when needed (already implemented)
- Consider using API-based embeddings instead of local model

### Option 3: Check for Memory Leaks
- Monitor `/api/health` endpoint to see memory over time
- Check if multiple agent instances are being created
- Ensure proper cleanup after requests

## Monitoring

Visit `/api/health` to see current memory usage:
```json
{
  "status": "healthy",
  "memory_mb": 229.03,
  "memory_percent": 44.7,
  "agent_loaded": true
}
```

