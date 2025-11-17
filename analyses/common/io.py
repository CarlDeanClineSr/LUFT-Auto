"""
IO utilities for LUFT Charter Symbiosis Pipeline.

Provides helpers for CSV, NPY, JSON file operations and directory management.
"""
import os
import json
import csv
import numpy as np
from pathlib import Path
from typing import Any, Dict, List, Union


def ensure_directory(path: Union[str, Path]) -> Path:
    """
    Ensure a directory exists, creating it if necessary.
    
    Args:
        path: Directory path to ensure exists
        
    Returns:
        Path object for the directory
    """
    path = Path(path)
    path.mkdir(parents=True, exist_ok=True)
    return path


def _convert_numpy_types(obj):
    """Convert numpy types to native Python types for JSON serialization."""
    if isinstance(obj, np.integer):
        return int(obj)
    elif isinstance(obj, np.floating):
        return float(obj)
    elif isinstance(obj, np.ndarray):
        return obj.tolist()
    elif isinstance(obj, np.bool_):
        return bool(obj)
    elif isinstance(obj, dict):
        return {key: _convert_numpy_types(value) for key, value in obj.items()}
    elif isinstance(obj, (list, tuple)):
        return [_convert_numpy_types(item) for item in obj]
    return obj


def save_json(data: Dict[str, Any], filepath: Union[str, Path]) -> None:
    """
    Save data to JSON file with pretty formatting.
    
    Handles numpy types by converting to native Python types.
    
    Args:
        data: Dictionary to save
        filepath: Output file path
    """
    filepath = Path(filepath)
    ensure_directory(filepath.parent)
    # Convert numpy types to native Python types
    data = _convert_numpy_types(data)
    with open(filepath, 'w') as f:
        json.dump(data, f, indent=2)


def load_json(filepath: Union[str, Path]) -> Dict[str, Any]:
    """
    Load data from JSON file.
    
    Args:
        filepath: Input file path
        
    Returns:
        Loaded dictionary
    """
    with open(filepath, 'r') as f:
        return json.load(f)


def save_npy(data: np.ndarray, filepath: Union[str, Path]) -> None:
    """
    Save numpy array to .npy file.
    
    Args:
        data: Numpy array to save
        filepath: Output file path
    """
    filepath = Path(filepath)
    ensure_directory(filepath.parent)
    np.save(filepath, data)


def load_npy(filepath: Union[str, Path]) -> np.ndarray:
    """
    Load numpy array from .npy file.
    
    Args:
        filepath: Input file path
        
    Returns:
        Loaded numpy array
    """
    return np.load(filepath)


def save_csv(data: List[Dict[str, Any]], filepath: Union[str, Path]) -> None:
    """
    Save list of dictionaries to CSV file.
    
    Args:
        data: List of dictionaries with consistent keys
        filepath: Output file path
    """
    if not data:
        return
    
    filepath = Path(filepath)
    ensure_directory(filepath.parent)
    
    fieldnames = list(data[0].keys())
    with open(filepath, 'w', newline='') as f:
        writer = csv.DictWriter(f, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerows(data)


def load_csv(filepath: Union[str, Path]) -> List[Dict[str, Any]]:
    """
    Load CSV file as list of dictionaries.
    
    Args:
        filepath: Input file path
        
    Returns:
        List of dictionaries
    """
    with open(filepath, 'r') as f:
        reader = csv.DictReader(f)
        return list(reader)
