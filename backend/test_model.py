"""
Test script for AI Portfolio Generator
Run this to test the model accuracy and generation quality
"""

import requests
import json
import time
from datetime import datetime

API_URL = "http://localhost:5000"

# Color codes for terminal output
class Colors:
    HEADER = '\033[95m'
    OKBLUE = '\033[94m'
    OKCYAN = '\033[96m'
    OKGREEN = '\033[92m'
    WARNING = '\033[93m'
    FAIL = '\033[91m'
    ENDC = '\033[0m'
    BOLD = '\033[1m'

def print_header(text):
    print(f"\n{Colors.HEADER}{Colors.BOLD}{'='*60}{Colors.ENDC}")
    print(f"{Colors.HEADER}{Colors.BOLD}{text.center(60)}{Colors.ENDC}")
    print(f"{Colors.HEADER}{Colors.BOLD}{'='*60}{Colors.ENDC}\n")

def print_success(text):
    print(f"{Colors.OKGREEN}✓ {text}{Colors.ENDC}")

def print_info(text):
    print(f"{Colors.OKCYAN}ℹ {text}{Colors.ENDC}")

def print_error(text):
    print(f"{Colors.FAIL}✗ {text}{Colors.ENDC}")

def print_warning(text):
    print(f"{Colors.WARNING}⚠ {text}{Colors.ENDC}")

def test_health_check():
    """Test if the API is running"""
    print_header("Testing API Health Check")
    try:
        response = requests.get(f"{API_URL}/health", timeout=5)
        if response.status_code == 200:
            data = response.json()
            print_success(f"API Status: {data['status']}")
            print_info(f"Model: {data['model']}")
            print_info(f"Device: {data['device']}")
            return True
        else:
            print_error(f"Health check failed with status {response.status_code}")
            return False
    except requests.exceptions.ConnectionError:
        print_error("Cannot connect to API. Make sure the backend is running!")
        return False
    except Exception as e:
        print_error(f"Error: {str(e)}")
        return False

def test_prompt_enhancement():
    """Test prompt enhancement endpoint"""
    print_header("Testing Prompt Enhancement")
    
    test_prompts = [
        "A cat",
        "Mountain landscape",
        "Portrait of a woman"
    ]
    
    for prompt in test_prompts:
        try:
            print_info(f"Original: {prompt}")
            response = requests.post(
                f"{API_URL}/enhance-prompt",
                json={"prompt": prompt},
                timeout=5
            )
            
            if response.status_code == 200:
                data = response.json()
                print_success(f"Enhanced: {data['enhanced']}")
            else:
                print_error(f"Enhancement failed: {response.text}")
        except Exception as e:
            print_error(f"Error: {str(e)}")
        print()

def test_image_generation():
    """Test image generation with various quality settings"""
    print_header("Testing Image Generation Quality")
    
    test_cases = [
        {
            "name": "🌅 Simple Landscape (Fast)",
            "prompt": "A serene mountain landscape at sunset",
            "steps": 30,
            "guidance_scale": 7.0,
            "description": "Quick generation with lower steps"
        },
        {
            "name": "👤 Detailed Portrait (Balanced)",
            "prompt": "Portrait of a young woman with flowing hair, studio lighting, professional photography",
            "negative_prompt": "blurry, distorted, deformed, disfigured",
            "steps": 50,
            "guidance_scale": 7.5,
            "description": "Recommended settings for quality"
        },
        {
            "name": "🏙️ Complex Scene (High Quality)",
            "prompt": "Futuristic cyberpunk city at night, neon lights, rain, highly detailed, cinematic",
            "negative_prompt": "blurry, low quality, pixelated",
            "steps": 75,
            "guidance_scale": 9.0,
            "description": "High quality settings for complex scenes"
        }
    ]
    
    results = []
    
    for test_case in test_cases:
        print(f"\n{Colors.BOLD}Testing: {test_case['name']}{Colors.ENDC}")
        print_info(f"Description: {test_case['description']}")
        print_info(f"Prompt: {test_case['prompt']}")
        print_info(f"Steps: {test_case['steps']}, Guidance: {test_case['guidance_scale']}")
        
        request_data = {
            "prompt": test_case["prompt"],
            "steps": test_case["steps"],
            "guidance_scale": test_case["guidance_scale"]
        }
        
        if "negative_prompt" in test_case:
            request_data["negative_prompt"] = test_case["negative_prompt"]
        
        try:
            start_time = time.time()
            response = requests.post(
                f"{API_URL}/generate",
                json=request_data,
                timeout=300  # 5 minutes timeout
            )
            end_time = time.time()
            generation_time = end_time - start_time
            
            if response.status_code == 200:
                data = response.json()
                print_success(f"Generation successful in {generation_time:.2f} seconds")
                print_info(f"Settings used: {data['settings']}")
                
                results.append({
                    "name": test_case["name"],
                    "time": generation_time,
                    "status": "success",
                    "settings": data['settings']
                })
            else:
                print_error(f"Generation failed: {response.text}")
                results.append({
                    "name": test_case["name"],
                    "status": "failed",
                    "error": response.text
                })
        
        except requests.exceptions.Timeout:
            print_error("Generation timed out (>5 minutes)")
            results.append({
                "name": test_case["name"],
                "status": "timeout"
            })
        except Exception as e:
            print_error(f"Error: {str(e)}")
            results.append({
                "name": test_case["name"],
                "status": "error",
                "error": str(e)
            })
    
    return results

def print_summary(results):
    """Print test summary"""
    print_header("Test Summary")
    
    successful = sum(1 for r in results if r.get('status') == 'success')
    failed = len(results) - successful
    
    print(f"{Colors.BOLD}Total Tests:{Colors.ENDC} {len(results)}")
    print_success(f"Successful: {successful}")
    if failed > 0:
        print_error(f"Failed: {failed}")
    
    if successful > 0:
        avg_time = sum(r['time'] for r in results if 'time' in r) / successful
        print_info(f"Average Generation Time: {avg_time:.2f} seconds")
    
    print("\n" + "="*60 + "\n")
    
    # Performance recommendations
    print(f"{Colors.BOLD}Performance Recommendations:{Colors.ENDC}\n")
    
    if avg_time < 10:
        print_success("Excellent performance! GPU acceleration is working well.")
    elif avg_time < 30:
        print_info("Good performance. Consider reducing steps if faster generation is needed.")
    else:
        print_warning("Slower performance detected. Check:")
        print("  - GPU is being used (check backend logs)")
        print("  - Reduce inference steps to 30-40 for faster generation")
        print("  - Ensure no other GPU-intensive tasks are running")

def run_performance_benchmark():
    """Run performance benchmark with different settings"""
    print_header("Performance Benchmark")
    
    step_counts = [20, 30, 50, 75]
    prompt = "A simple landscape with mountains"
    
    print_info("Testing generation speed with different step counts...\n")
    
    for steps in step_counts:
        try:
            start_time = time.time()
            response = requests.post(
                f"{API_URL}/generate",
                json={
                    "prompt": prompt,
                    "steps": steps,
                    "guidance_scale": 7.5
                },
                timeout=300
            )
            end_time = time.time()
            
            if response.status_code == 200:
                time_taken = end_time - start_time
                time_per_step = time_taken / steps
                print_success(f"Steps: {steps:3d} | Time: {time_taken:6.2f}s | Per Step: {time_per_step:.3f}s")
        except Exception as e:
            print_error(f"Steps: {steps:3d} | Failed: {str(e)}")

def main():
    """Main test runner"""
    print(f"\n{Colors.BOLD}{Colors.HEADER}")
    print("╔══════════════════════════════════════════════════════════╗")
    print("║                                                          ║")
    print("║        AI Portfolio Generator - Test Suite              ║")
    print("║                                                          ║")
    print("╚══════════════════════════════════════════════════════════╝")
    print(f"{Colors.ENDC}\n")
    
    print_info(f"Test started at: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    print_info(f"API URL: {API_URL}\n")
    
    # Test 1: Health Check
    if not test_health_check():
        print_error("\nBackend is not running. Please start it with:")
        print_info("  cd backend")
        print_info("  python app.py")
        return
    
    # Test 2: Prompt Enhancement
    test_prompt_enhancement()
    
    # Test 3: Image Generation
    print_warning("Starting image generation tests. This may take several minutes...")
    results = test_image_generation()
    
    # Test 4: Performance Benchmark
    response = input(f"\n{Colors.BOLD}Run performance benchmark? (y/n): {Colors.ENDC}")
    if response.lower() == 'y':
        run_performance_benchmark()
    
    # Print Summary
    print_summary(results)
    
    print_info(f"Test completed at: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    print(f"\n{Colors.OKGREEN}✓ All tests completed!{Colors.ENDC}\n")

if __name__ == "__main__":
    main()
