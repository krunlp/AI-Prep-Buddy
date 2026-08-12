---
layout: default
title: Code Solutions
---
# Navigation Bar
[Home](./) | [System Design](./system-design.md) | [Code Solutions](./code-solutions.md)

### Q981. Implement k-means clustering from scratch

**Key Concepts**: 
- Initializing centroids
- Assigning points to nearest centroids
- Updating centroids based on cluster means

```python
import numpy as np

def kmeans(X, k, max_iters=100):
    """
    Implements K-Means clustering.
    X: np.array of shape (n_samples, n_features)
    k: int, number of clusters
    """
    # Randomly initialize centroids from data points
    idx = np.random.choice(len(X), k, replace=False)
    centroids = X[idx]
    
    for _ in range(max_iters):
        # Calculate distances from each point to each centroid
        distances = np.linalg.norm(X[:, np.newaxis] - centroids, axis=2)
        
        # Assign points to closest centroid
        labels = np.argmin(distances, axis=1)
        
        # Calculate new centroids
        new_centroids = np.array([X[labels == i].mean(axis=0) if len(X[labels == i]) > 0 else centroids[i] for i in range(k)])
        
        # Check for convergence
        if np.allclose(centroids, new_centroids):
            break
            
        centroids = new_centroids
        
    return labels, centroids
```

**Complexity**: Time O(max_iters * n_samples * k * n_features), Space O(n_samples + k * n_features)
**Interview Tips**: Ensure you handle empty clusters during the update step (e.g., fallback to the previous centroid).

### Q982. Implement logistic regression gradient descent

**Key Concepts**: 
- Sigmoid activation function
- Binary cross-entropy loss gradient
- Iterative weight updates

```python
import numpy as np

def sigmoid(z):
    return 1 / (1 + np.exp(-z))

def logistic_regression(X, y, lr=0.01, epochs=1000):
    """
    Implements Logistic Regression using Gradient Descent.
    X: np.array of shape (n_samples, n_features)
    y: np.array of shape (n_samples,) binary labels
    """
    n_samples, n_features = X.shape
    weights = np.zeros(n_features)
    bias = 0
    
    for _ in range(epochs):
        # Forward pass
        linear_model = np.dot(X, weights) + bias
        predictions = sigmoid(linear_model)
        
        # Gradients
        dw = (1 / n_samples) * np.dot(X.T, (predictions - y))
        db = (1 / n_samples) * np.sum(predictions - y)
        
        # Update weights
        weights -= lr * dw
        bias -= lr * db
        
    return weights, bias
```

**Complexity**: Time O(epochs * n_samples * n_features), Space O(n_features)
**Interview Tips**: Remember the gradient of BCE loss with sigmoid simplifies elegantly to `predictions - y`.

### Q983. Confusion matrix + precision/recall/F1

**Key Concepts**: 
- True/False Positives/Negatives
- Metric definitions
- Zero division handling

```python
import numpy as np

def classification_metrics(y_true, y_pred):
    """
    Calculates confusion matrix and related metrics for binary classification.
    """
    tp = np.sum((y_true == 1) & (y_pred == 1))
    tn = np.sum((y_true == 0) & (y_pred == 0))
    fp = np.sum((y_true == 0) & (y_pred == 1))
    fn = np.sum((y_true == 1) & (y_pred == 0))
    
    # Safe division to prevent ZeroDivisionError
    precision = tp / (tp + fp) if (tp + fp) > 0 else 0.0
    recall = tp / (tp + fn) if (tp + fn) > 0 else 0.0
    
    f1 = 2 * (precision * recall) / (precision + recall) if (precision + recall) > 0 else 0.0
    
    return {
        'confusion_matrix': [[tn, fp], [fn, tp]],
        'precision': precision,
        'recall': recall,
        'f1': f1
    }
```

**Complexity**: Time O(n), Space O(1)
**Interview Tips**: Interviewers often check if you remember to handle edge cases like 0 denominators in precision/recall calculation.

### Q984. Decision tree split (Gini or entropy)

**Key Concepts**: 
- Information gain calculation
- Class probabilities
- Identifying the best split threshold

```python
import numpy as np

def calculate_gini(labels):
    """Calculates Gini impurity of a set of labels."""
    if len(labels) == 0:
        return 0
    counts = np.bincount(labels)
    probabilities = counts / len(labels)
    return 1 - np.sum(probabilities ** 2)

def best_split(X, y, feature_idx):
    """Finds the best threshold to split a specific feature."""
    best_gini = float('inf')
    best_threshold = None
    
    # Sort data based on feature
    sorted_indices = np.argsort(X[:, feature_idx])
    sorted_x = X[sorted_indices, feature_idx]
    sorted_y = y[sorted_indices]
    
    # Check possible split points
    for i in range(1, len(sorted_y)):
        if sorted_x[i] == sorted_x[i-1]:
            continue # Skip identical values
            
        left_y = sorted_y[:i]
        right_y = sorted_y[i:]
        
        # Calculate weighted Gini
        n = len(y)
        gini = (len(left_y) / n) * calculate_gini(left_y) + (len(right_y) / n) * calculate_gini(right_y)
        
        if gini < best_gini:
            best_gini = gini
            best_threshold = (sorted_x[i] + sorted_x[i-1]) / 2
            
    return best_threshold, best_gini
```

**Complexity**: Time O(n log n) per feature due to sorting, Space O(n)
**Interview Tips**: Sorting the feature values first allows for efficient sequential evaluation of split points.

### Q985. Cosine similarity at scale

**Key Concepts**: 
- Vector normalization
- Matrix multiplication
- Broadcasting

```python
import numpy as np

def cosine_similarity_matrix(A, B):
    """
    Computes cosine similarity between all pairs in A and B.
    A: np.array of shape (m, d)
    B: np.array of shape (n, d)
    Returns matrix of shape (m, n)
    """
    # Compute dot products
    dot_products = np.dot(A, B.T)
    
    # Compute L2 norms
    norm_A = np.linalg.norm(A, axis=1, keepdims=True)
    norm_B = np.linalg.norm(B, axis=1, keepdims=True)
    
    # Avoid division by zero
    norm_A[norm_A == 0] = 1e-10
    norm_B[norm_B == 0] = 1e-10
    
    # Calculate similarity
    similarity = dot_products / (norm_A * norm_B.T)
    
    return similarity
```

**Complexity**: Time O(m * n * d), Space O(m * n)
**Interview Tips**: Vectorizing the calculation using matrix multiplication is essential for scaling compared to nested loops.

### Q986. K-nearest-neighbors classifier

**Key Concepts**: 
- Distance calculation
- Finding top k elements
- Majority voting

```python
import numpy as np
from collections import Counter

class KNNClassifier:
    def __init__(self, k=3):
        self.k = k
        
    def fit(self, X_train, y_train):
        # KNN is a lazy learner, so we just store the data
        self.X_train = X_train
        self.y_train = y_train
        
    def predict(self, X_test):
        predictions = []
        for x in X_test:
            # Calculate distances to all training points
            distances = np.linalg.norm(self.X_train - x, axis=1)
            
            # Get indices of top k smallest distances
            k_indices = np.argsort(distances)[:self.k]
            
            # Get corresponding labels
            k_nearest_labels = self.y_train[k_indices]
            
            # Majority vote
            most_common = Counter(k_nearest_labels).most_common(1)
            predictions.append(most_common[0][0])
            
        return np.array(predictions)
```

**Complexity**: Time O(n_test * n_train * d), Space O(n_train * d)
**Interview Tips**: Note that training is O(1) but prediction is O(N) unless you optimize with spatial structures like KD-Trees.

### Q987. Class imbalance via weighted sampling

**Key Concepts**: 
- Class frequencies
- Inverse frequency weighting
- Sampling with probabilities

```python
import numpy as np

def get_balanced_sampler(labels, batch_size):
    """
    Creates a sampler that returns balanced batches from imbalanced data.
    """
    classes, counts = np.unique(labels, return_counts=True)
    
    # Calculate weights: inversely proportional to class frequency
    class_weights = 1.0 / counts
    weight_map = dict(zip(classes, class_weights))
    
    # Assign weight to each sample
    sample_weights = np.array([weight_map[label] for label in labels])
    
    # Normalize probabilities
    sample_probs = sample_weights / np.sum(sample_weights)
    
    def sample_batch():
        # Sample indices based on probabilities
        indices = np.random.choice(len(labels), size=batch_size, replace=True, p=sample_probs)
        return indices
        
    return sample_batch
```

**Complexity**: Time O(N) to setup, O(batch_size * log N) per sample call; Space O(N)
**Interview Tips**: Explain how `replace=True` is crucial here because minority classes need to be oversampled.

### Q988. Scaled dot-product attention (NumPy/PyTorch)

**Key Concepts**: 
- Q, K, V matrices
- Scaling by sqrt(d_k)
- Softmax and masking

```python
import torch
import torch.nn.functional as F
import math

def scaled_dot_product_attention(query, key, value, mask=None):
    """
    Computes scaled dot-product attention.
    query, key, value: tensors of shape (batch, seq_len, d_k)
    """
    d_k = query.size(-1)
    
    # Compute attention scores: Q * K^T / sqrt(d_k)
    # query: (b, s, d), key: (b, s, d) -> key.transpose(-2, -1): (b, d, s)
    # scores: (b, s, s)
    scores = torch.matmul(query, key.transpose(-2, -1)) / math.sqrt(d_k)
    
    if mask is not None:
        # Apply mask (e.g., for causal attention)
        scores = scores.masked_fill(mask == 0, float('-inf'))
        
    # Apply softmax to get probabilities
    attention_weights = F.softmax(scores, dim=-1)
    
    # Multiply by values: attention * V
    output = torch.matmul(attention_weights, value)
    
    return output, attention_weights
```

**Complexity**: Time O(batch * seq_len^2 * d_k), Space O(batch * seq_len^2)
**Interview Tips**: Emphasize why the `sqrt(d_k)` scaling is necessary (it prevents softmax from pushing gradients to zero for large dimensions).

### Q989. BPE-style tokenizer

**Key Concepts**: 
- Character-level initialization
- Finding most frequent pairs
- Merging pairs

```python
from collections import Counter

def get_stats(vocab):
    """Counts frequency of adjacent symbol pairs."""
    pairs = Counter()
    for word, freq in vocab.items():
        symbols = word.split()
        for i in range(len(symbols) - 1):
            pairs[symbols[i], symbols[i+1]] += freq
    return pairs

def merge_vocab(pair, v_in):
    """Merges the most frequent pair in the vocabulary."""
    v_out = {}
    bigram = ' '.join(pair)
    replacement = ''.join(pair)
    
    for word, freq in v_in.items():
        # Replace occurrences of the bigram
        new_word = word.replace(bigram, replacement)
        v_out[new_word] = freq
    return v_out

def learn_bpe(corpus, num_merges):
    # Initialize vocab with spaces between chars
    vocab = Counter(' '.join(list(word)) + ' </w>' for word in corpus.split())
    
    merges = []
    for i in range(num_merges):
        pairs = get_stats(vocab)
        if not pairs:
            break
            
        best_pair = max(pairs, key=pairs.get)
        vocab = merge_vocab(best_pair, vocab)
        merges.append(best_pair)
        
    return merges, vocab
```

**Complexity**: Time O(num_merges * vocab_size * max_word_length), Space O(vocab_size)
**Interview Tips**: BPE operates on subwords, allowing models to handle out-of-vocabulary words gracefully.

### Q990. Top-k and top-p (nucleus) sampling

**Key Concepts**: 
- Filtering logits based on rank (top-k)
- Filtering logits based on cumulative probability (top-p)

```python
import torch
import torch.nn.functional as F

def sample_logits(logits, top_k=0, top_p=0.0, temperature=1.0):
    """
    Applies temperature, top-k, and top-p filtering to logits, then samples.
    logits: 1D tensor of shape (vocab_size,)
    """
    logits = logits / temperature
    
    if top_k > 0:
        # Keep only top_k logits, set others to -inf
        indices_to_remove = logits < torch.topk(logits, top_k)[0][..., -1, None]
        logits[indices_to_remove] = float('-inf')
        
    if top_p > 0.0:
        sorted_logits, sorted_indices = torch.sort(logits, descending=True)
        cumulative_probs = torch.cumsum(F.softmax(sorted_logits, dim=-1), dim=-1)
        
        # Remove tokens with cumulative probability above the threshold
        sorted_indices_to_remove = cumulative_probs > top_p
        # Shift to keep the first token that exceeds the threshold
        sorted_indices_to_remove[..., 1:] = sorted_indices_to_remove[..., :-1].clone()
        sorted_indices_to_remove[..., 0] = 0
        
        indices_to_remove = sorted_indices[sorted_indices_to_remove]
        logits[indices_to_remove] = float('-inf')
        
    probs = F.softmax(logits, dim=-1)
    return torch.multinomial(probs, num_samples=1)
```

**Complexity**: Time O(V log V) where V is vocab size due to sorting, Space O(V)
**Interview Tips**: Mention that top-p adapts to the distribution's shape better than top-k (dynamic cutoff vs static).

### Q991. SQL: rolling 7-day retention

**Key Concepts**: 
- Self-joins or window functions
- Date arithmetic

```sql
-- Assuming table: user_activity (user_id, activity_date)
WITH distinct_activity AS (
    SELECT DISTINCT user_id, activity_date
    FROM user_activity
)
SELECT 
    a1.activity_date AS signup_date,
    COUNT(DISTINCT a1.user_id) AS total_users,
    COUNT(DISTINCT a2.user_id) AS retained_users,
    CAST(COUNT(DISTINCT a2.user_id) AS FLOAT) / COUNT(DISTINCT a1.user_id) AS retention_rate
FROM distinct_activity a1
LEFT JOIN distinct_activity a2 
    ON a1.user_id = a2.user_id 
    AND a2.activity_date = DATE_ADD(a1.activity_date, INTERVAL 7 DAY)
GROUP BY a1.activity_date
ORDER BY a1.activity_date;
```

**Complexity**: Depends on DB, typically O(N log N) or O(N) with hash joins.
**Interview Tips**: Clarify if "7-day retention" means exactly on day 7, or within 7 days. The above checks exactly day 7.

### Q992. SQL: detect duplicate near-matches

**Key Concepts**: 
- Levenshtein distance
- String matching

```sql
-- Assuming table: products (id, name)
-- Find products with similar names using Levenshtein distance (supported in Postgres/some dialects)
SELECT 
    p1.id AS id1, 
    p1.name AS name1,
    p2.id AS id2,
    p2.name AS name2,
    LEVENSHTEIN(p1.name, p2.name) AS distance
FROM products p1
JOIN products p2 
    ON p1.id < p2.id -- avoid A-B and B-A duplicates, and self-matches
WHERE LEVENSHTEIN(p1.name, p2.name) <= 3
ORDER BY distance;

-- Alternative if Levenshtein is not available (using SOUNDEX):
SELECT p1.id, p1.name, p2.id, p2.name
FROM products p1
JOIN products p2 
    ON p1.id < p2.id 
    AND SOUNDEX(p1.name) = SOUNDEX(p2.name);
```

**Complexity**: O(N^2) naive, typically optimized via blocking/indexing in practice.
**Interview Tips**: Mention that N^2 cross joins are bad for large tables; in real systems, use a blocked approach or locality-sensitive hashing (LSH).

### Q993. LRU cache

**Key Concepts**: 
- Hash map for O(1) access
- Doubly linked list for O(1) eviction
- Python's `OrderedDict`

```python
from collections import OrderedDict

class LRUCache:
    def __init__(self, capacity: int):
        self.cache = OrderedDict()
        self.capacity = capacity

    def get(self, key: int) -> int:
        if key not in self.cache:
            return -1
        # Move the accessed item to the end (most recently used)
        self.cache.move_to_end(key)
        return self.cache[key]

    def put(self, key: int, value: int) -> None:
        if key in self.cache:
            # Update value and mark as recently used
            self.cache.move_to_end(key)
        self.cache[key] = value
        
        # Evict least recently used if capacity exceeded
        if len(self.cache) > self.capacity:
            # popitem(last=False) removes the first item (least recently used)
            self.cache.popitem(last=False)
```

**Complexity**: Time O(1) for both get and put, Space O(capacity)
**Interview Tips**: In Python, `OrderedDict` is the standard way to implement this concisely. Be prepared to explain how to build it from scratch using a dict and a custom doubly linked list.

### Q994. Document chunking with overlapping windows

**Key Concepts**: 
- Context windows
- Overlap handling
- Tokenization limits

```python
def chunk_text(text, chunk_size, overlap):
    """
    Splits text into chunks of `chunk_size` words with `overlap` words.
    """
    words = text.split()
    chunks = []
    
    if len(words) <= chunk_size:
        return [text]
        
    step = chunk_size - overlap
    if step <= 0:
        raise ValueError("Overlap must be less than chunk size")
        
    for i in range(0, len(words) - overlap, step):
        chunk = words[i:i + chunk_size]
        chunks.append(" ".join(chunk))
        
        # Break if we've reached the end
        if i + chunk_size >= len(words):
            break
            
    return chunks

# Example: chunk_size=5, overlap=2
# text = "the quick brown fox jumps over the lazy dog"
# chunks = ["the quick brown fox jumps", "fox jumps over the lazy", "the lazy dog"]
```

**Complexity**: Time O(N), Space O(N) where N is number of words
**Interview Tips**: Chunking is critical for RAG (Retrieval-Augmented Generation) pipelines to maintain context across chunk boundaries.

### Q995. Priority queue for top-N recommendations

**Key Concepts**: 
- Min-heap
- Keeping bounded size for efficiency

```python
import heapq

def get_top_n_recommendations(user_scores, n):
    """
    Finds top N items using a min-heap.
    user_scores: list of tuples (score, item_id)
    """
    min_heap = []
    
    for score, item_id in user_scores:
        if len(min_heap) < n:
            heapq.heappush(min_heap, (score, item_id))
        else:
            # If current score is greater than the smallest in heap
            if score > min_heap[0][0]:
                heapq.heappushpop(min_heap, (score, item_id))
                
    # Sort descending for final output
    return sorted(min_heap, key=lambda x: x[0], reverse=True)
```

**Complexity**: Time O(M log N) where M is total items, Space O(N)
**Interview Tips**: Using a min-heap of size N is much faster than sorting the entire list O(M log M) when N is much smaller than M.

### Q996. Batch API requests with retry/backoff

**Key Concepts**: 
- Exponential backoff
- Concurrency
- Exception handling

```python
import time
import random

def call_api_with_retry(item, max_retries=3, base_delay=1.0):
    """Simulates an API call with exponential backoff."""
    for attempt in range(max_retries):
        try:
            # Simulate network call that might fail randomly
            if random.random() < 0.3:
                raise ConnectionError("Temporary failure")
            return f"Success for {item}"
            
        except Exception as e:
            if attempt == max_retries - 1:
                return f"Failed for {item} after {max_retries} attempts"
                
            # Exponential backoff with jitter
            delay = base_delay * (2 ** attempt) + random.uniform(0, 0.5)
            time.sleep(delay)

def process_batch(items):
    # In a real scenario, use ThreadPoolExecutor or asyncio
    results = []
    for item in items:
        results.append(call_api_with_retry(item))
    return results
```

**Complexity**: Time O(N * retries), Space O(N) for results
**Interview Tips**: Mention "jitter" (adding random noise to the delay) to prevent the "thundering herd" problem when many requests retry simultaneously.

### Q997. A/B test significance calculator

**Key Concepts**: 
- Z-test for proportions
- Statistical significance (p-value)

```python
import math
from scipy.stats import norm

def ab_test_significance(visitors_A, conversions_A, visitors_B, conversions_B, alpha=0.05):
    """Calculates if variation B is significantly different from A."""
    
    # Conversion rates
    p_A = conversions_A / visitors_A
    p_B = conversions_B / visitors_B
    
    # Pooled probability
    p_pool = (conversions_A + conversions_B) / (visitors_A + visitors_B)
    
    # Standard error
    se = math.sqrt(p_pool * (1 - p_pool) * (1 / visitors_A + 1 / visitors_B))
    
    # Z-score
    z_score = (p_B - p_A) / se
    
    # P-value (two-tailed)
    p_value = 2 * (1 - norm.cdf(abs(z_score)))
    
    is_significant = p_value < alpha
    
    return {
        'z_score': z_score,
        'p_value': p_value,
        'significant': is_significant,
        'uplift': (p_B - p_A) / p_A
    }
```

**Complexity**: Time O(1), Space O(1)
**Interview Tips**: Know the assumptions: this relies on normal approximation, which is valid when sample sizes are sufficiently large (np > 5 and n(1-p) > 5).

### Q998. Deduplicate embeddings above similarity threshold

**Key Concepts**: 
- Pairwise similarity
- Connected components / clustering

```python
import numpy as np

def deduplicate_embeddings(embeddings, threshold=0.95):
    """
    Keeps only one embedding from any group that is highly similar.
    embeddings: np.array of shape (N, D)
    """
    # Normalize for cosine similarity
    norms = np.linalg.norm(embeddings, axis=1, keepdims=True)
    normalized_embs = embeddings / np.maximum(norms, 1e-10)
    
    # Compute full similarity matrix (N, N)
    sim_matrix = np.dot(normalized_embs, normalized_embs.T)
    
    keep_indices = []
    dropped = set()
    
    for i in range(len(embeddings)):
        if i in dropped:
            continue
            
        keep_indices.append(i)
        
        # Find all items similar to item i
        similar_items = np.where(sim_matrix[i] >= threshold)[0]
        
        for j in similar_items:
            if j != i:
                dropped.add(j)
                
    return embeddings[keep_indices], keep_indices
```

**Complexity**: Time O(N^2 * D), Space O(N^2) for the similarity matrix
**Interview Tips**: For very large N, explicitly computing the N^2 matrix is a bottleneck. Mention Faiss or HNSW for scalable approximate nearest neighbor search.

### Q999. Gradient checking

**Key Concepts**: 
- Numerical vs analytical gradients
- Finite difference approximation

```python
import numpy as np

def gradient_check(func, grad_func, x, epsilon=1e-5, tolerance=1e-7):
    """
    Checks if the analytical gradient matches the numerical gradient.
    func: f(x) -> scalar
    grad_func: f'(x) -> vector
    x: input vector
    """
    analytical_grad = grad_func(x)
    numerical_grad = np.zeros_like(x)
    
    for i in range(len(x)):
        # Create perturbed vectors
        x_plus = np.copy(x)
        x_minus = np.copy(x)
        
        x_plus[i] += epsilon
        x_minus[i] -= epsilon
        
        # Compute numerical derivative (centered difference)
        numerical_grad[i] = (func(x_plus) - func(x_minus)) / (2 * epsilon)
        
    # Compute relative error
    numerator = np.linalg.norm(analytical_grad - numerical_grad)
    denominator = np.linalg.norm(analytical_grad) + np.linalg.norm(numerical_grad)
    
    relative_error = numerator / denominator if denominator != 0 else 0
    
    is_correct = relative_error < tolerance
    return is_correct, relative_error
```

**Complexity**: Time O(N * cost of func) where N is params, Space O(N)
**Interview Tips**: Used primarily for debugging custom autograd implementations or complex backprop derivations.

### Q1000. Parse/validate LLM JSON output

**Key Concepts**: 
- Regular expressions
- JSON parsing
- Fallbacks

```python
import json
import re

def parse_llm_json(llm_output, required_keys=None):
    """
    Attempts to extract and parse JSON from a noisy LLM response.
    """
    # Try to find a JSON block using regex (handles markdown backticks)
    json_match = re.search(r'```(?:json)?\s*(\{.*?\})\s*```', llm_output, re.DOTALL)
    
    if json_match:
        json_str = json_match.group(1)
    else:
        # Fallback: look for the first { and last }
        start = llm_output.find('{')
        end = llm_output.rfind('}')
        if start != -1 and end != -1 and end > start:
            json_str = llm_output[start:end+1]
        else:
            return None, "No JSON object found."
            
    try:
        data = json.loads(json_str)
        
        # Validate schema
        if required_keys:
            missing_keys = [k for k in required_keys if k not in data]
            if missing_keys:
                return None, f"Missing required keys: {missing_keys}"
                
        return data, "Success"
    except json.JSONDecodeError as e:
        return None, f"JSON parsing failed: {str(e)}"
```

**Complexity**: Time O(L) where L is string length, Space O(L)
**Interview Tips**: Modern LLM pipelines often use structured outputs (like OpenAI's function calling) to avoid regex hacking, but parsing raw output remains a common fallback.

### Q1001. Circular buffer

**Key Concepts**: 
- Fixed-size array
- Modulo arithmetic for pointers

```python
class CircularBuffer:
    def __init__(self, capacity):
        self.buffer = [None] * capacity
        self.capacity = capacity
        self.head = 0  # Write pointer
        self.tail = 0  # Read pointer
        self.size = 0
        
    def enqueue(self, item):
        if self.is_full():
            # Overwrite oldest data
            self.tail = (self.tail + 1) % self.capacity
        else:
            self.size += 1
            
        self.buffer[self.head] = item
        self.head = (self.head + 1) % self.capacity
        
    def dequeue(self):
        if self.is_empty():
            raise IndexError("Buffer is empty")
            
        item = self.buffer[self.tail]
        self.buffer[self.tail] = None
        self.tail = (self.tail + 1) % self.capacity
        self.size -= 1
        return item
        
    def is_full(self):
        return self.size == self.capacity
        
    def is_empty(self):
        return self.size == 0
```

**Complexity**: Time O(1) ops, Space O(capacity)
**Interview Tips**: Used heavily in streaming data, audio processing, and networking.

### Q1002. Exponential moving average for streaming metrics

**Key Concepts**: 
- Memoryless smoothing
- Decay factor

```python
class ExponentialMovingAverage:
    def __init__(self, alpha=0.1):
        """
        alpha: smoothing factor (0 < alpha < 1)
        High alpha discounts older observations faster.
        """
        if not (0 < alpha <= 1):
            raise ValueError("Alpha must be between 0 and 1")
        self.alpha = alpha
        self.ema = None
        
    def update(self, value):
        if self.ema is None:
            self.ema = float(value)
        else:
            # EMA_t = alpha * value_t + (1 - alpha) * EMA_{t-1}
            self.ema = self.alpha * value + (1 - self.alpha) * self.ema
        return self.ema
        
    def get(self):
        return self.ema

# Example usage for tracking latency
# tracker = ExponentialMovingAverage(alpha=0.05)
# for latency in stream: tracker.update(latency)
```

**Complexity**: Time O(1), Space O(1)
**Interview Tips**: EMA is preferred over simple moving average (SMA) for streaming because it requires O(1) memory instead of O(W) where W is the window size.

### Q1003. Beam search decoder

**Key Concepts**: 
- Expanding top sequences
- Keeping beam width bounded
- Sequence scoring

```python
import numpy as np

def beam_search_decoder(model_predict_fn, start_token, end_token, max_len, beam_width):
    """
    Simulates beam search for sequence generation.
    model_predict_fn: func(sequence) -> log_probs of next tokens
    """
    # Store tuples of (sequence, total_log_prob)
    sequences = [([start_token], 0.0)]
    
    for _ in range(max_len):
        all_candidates = []
        
        # Expand each sequence in the current beam
        for seq, score in sequences:
            if seq[-1] == end_token:
                all_candidates.append((seq, score))
                continue
                
            # Get log probabilities for next token
            log_probs = model_predict_fn(seq)
            
            # Add top candidates (simplified: taking all here, slicing later)
            for token_id, token_log_prob in enumerate(log_probs):
                candidate_seq = seq + [token_id]
                candidate_score = score + token_log_prob
                all_candidates.append((candidate_seq, candidate_score))
                
        # Sort candidates by score (descending)
        ordered = sorted(all_candidates, key=lambda x: x[1], reverse=True)
        
        # Keep top 'beam_width' sequences
        sequences = ordered[:beam_width]
        
        # Early stopping if all beams hit end token
        if all(seq[-1] == end_token for seq, _ in sequences):
            break
            
    return sequences[0] # Return the best sequence
```

**Complexity**: Time O(max_len * beam_width * vocab_size), Space O(beam_width * max_len)
**Interview Tips**: Note that beam search doesn't guarantee the global optimal sequence, but it's a strong heuristic. Normalizing scores by sequence length prevents penalizing longer sequences.

### Q1004. SQL: cohort-based churn rate

**Key Concepts**: 
- Defining cohorts (e.g., signup month)
- Grouping by tenure

```sql
-- Assuming tables: users (id, signup_date), events (user_id, event_date)
WITH cohorts AS (
    SELECT 
        id AS user_id, 
        DATE_TRUNC('month', signup_date) AS cohort_month
    FROM users
),
activity AS (
    SELECT 
        user_id, 
        DATE_TRUNC('month', event_date) AS active_month
    FROM events
    GROUP BY 1, 2
),
cohort_sizes AS (
    SELECT cohort_month, COUNT(DISTINCT user_id) AS total_users
    FROM cohorts
    GROUP BY 1
)
SELECT 
    c.cohort_month,
    EXTRACT(MONTH FROM AGE(a.active_month, c.cohort_month)) AS month_number,
    cs.total_users,
    COUNT(DISTINCT a.user_id) AS active_users,
    1.0 - (CAST(COUNT(DISTINCT a.user_id) AS FLOAT) / cs.total_users) AS churn_rate
FROM cohorts c
JOIN activity a ON c.user_id = a.user_id
JOIN cohort_sizes cs ON c.cohort_month = cs.cohort_month
GROUP BY 1, 2, 3
ORDER BY 1, 2;
```

**Complexity**: O(N log N) for grouping/sorting
**Interview Tips**: A standard product analytics query. AGE() or similar functions are dialect-specific (PostgreSQL shown here).

### Q1005. Reservoir sampling

**Key Concepts**: 
- Random sampling from unknown length stream
- Guaranteeing uniform probability

```python
import random

def reservoir_sampling(stream, k):
    """
    Selects k items uniformly at random from a stream of unknown size.
    """
    reservoir = []
    
    for i, item in enumerate(stream):
        # Fill the reservoir with the first k items
        if i < k:
            reservoir.append(item)
        else:
            # For the i-th item (0-indexed), replace a random item 
            # in the reservoir with probability k / (i + 1)
            j = random.randint(0, i)
            if j < k:
                reservoir[j] = item
                
    return reservoir
```

**Complexity**: Time O(N) where N is stream length, Space O(k)
**Interview Tips**: Be able to prove mathematically why this guarantees uniform probability for every item in the stream. (The probability an item is chosen and survives all subsequent replacements is exactly k/N).
